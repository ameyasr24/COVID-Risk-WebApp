import numpy as np
import pandas as pd
import math
import getCountyCases from getCountyCases

e = math.e

volume = 9000
num_faculty = 1
num_students = 10
duration = 75
num_class_periods = 26
breathing_rate_faculty = [0.027,0.029]
breathing_rate_student = [0.012,0.012]
ventilation_w_outside_air = [1,4]
decay_rate_of_virus = [0,1.0]
deposition_to_surface = [0.3,1.5]
additional_control_measures = [0,0]
quanta_emission_rate_faculty = [1.5,0.71]
quanta_emission_rate_student = [0.69,0.71]
exhalation_mask_efficiency = [0.4,0.6]
inhalation_mask_efficiency = [0.3,0.5]
background_infection_rate_faculty = [0.0070,0.0140]
background_infection_rate_student = [0.0070,0.0140]

county = ""
state = ""
percent_faculty_infectious = getCountyCases(county, state)
percent_student_infectious = getCountyCases(county, state)

############################
trials = 100000
fac_runs = []
student_runs = []
for(x in range trials):
    randomizeAll()
    cf = calc_Cf(quanta_emission_rate_faculty, exhalation_mask_efficiency, (ventilation_w_outside_air+decay_rate_of_virus+deposition_to_surface+additional_control_measures), duration)
    cs = calc_Cs(quanta_emission_rate_student, exhalation_mask_efficiency, (ventilation_w_outside_air+decay_rate_of_virus+deposition_to_surface+additional_control_measures), duration)
    Nfs = calc_Nfs(cf, background_infection_rate_student, inhalation_mask_efficiency, duration)
    Nsf = calc_Nsf(cs, background_infection_rate_student, inhalation_mask_efficiency, duration)
    Nss = calc_Nss(cs, background_infection_rate_student, inhalation_mask_efficiency, duration)
    Pfs = calc_pfs(percent_faculty_infectious, Nfs)
    Psf = calc_psf(percent_student_infectious, Nsf)
    Pss = calc_pss(percent_student_infectious, Nss)
    P1f = calc_p1f(Psf, num_students)
    P1s = calc_p1s(Pss, num_students, Pfs, num_faculty)
    Pf = calc_pf(P1f, num_class_periods)
    Ps = calc_ps(P1s, num_class_periods)
    fac_runs[x] = Pf
    student_runs[x] = Ps

def randomizeAll():
    randomize(breathing_rate_faculty)
    randomize(breathing_rate_student)
    randomize(ventilation_w_outside_air)
    randomize(decay_rate_of_virus)
    randomize(deposition_to_surface)
    randomize(additional_control_measures)
    randomize(exhalation_mask_efficiency)
    randomize(inhalation_mask_efficiency)
    randomize(background_infection_rate_faculty)
    randomize(background_infection_rate_student)
    
    randomizeFromNormal(quanta_emission_rate_faculty)
    randomizeFromNormal(quanta_emission_rate_student)


def randomize(bounds):
    bounds[2] = np.random() * bounds[1]-bounds[0]

def randomizeFromNormal(normdist):
    normdist[2] = 10**np.random.normal(normdist[0],normdist[1])
    ##also does the UNDO LOG

# Q_f: quanta emission rate by infected faculty 
# m_out: mask exhalation efficiency 
# k: first order loss coefficients for ventilation , decay, deposition, and other control measures
# V: volume of classroom
# T: duration of each in-person class session 

# Average quanta concentration during class period if 1 faculty member is infected: 
def calc_Cf(Q_f,m_out,k,V,T):
    cf = ((Q_f*(1-m_out))/(k*V))*(1-(1/(k*T))*(1-e**(-k*T)))
    return cf

# Average quanta concentration during class period if 1 student is infected: 
def calc_Cs(Q_s,m_out,k,V,T):
    cs = ((Q_s*(1-m_out))/(k*V))*(1-(1/(k*T))*(1-e**(-k*T)))
    return cs

# Quanta inhaled by student if 1 faculty infected:
def calc_Nfs(C_f,I_s,m_in,T):
    Nfs = C_f*I_s*(1-m_in)*T
    return Nfs

# Quanta inhaled by faculty if 1 student infected:
def calc_Nsf(C_s,I_f,m_in,T):
    Nsf = C_s*I_f*(1-m_in)*T
    return Nsf

# Quanta inhaled by student if 1 student infected
def calc_Nss(C_s,I_s,m_in,T):
    Nss = C_s*I_s*(1-m_in)*T
    return Nss

# Probability of 1 faculty infecting student:
def calc_pfs(f_f,N_fs):
    pfs = f_f*(1-e**(-N_fs))
    return pfs

# Probability of 1 student infecting faculty:
def calc_psf(f_s,N_sf):
    psf = f_s*(1-e**(-N_sf))
    return psf

# Probability of 1 student infecting student: 
def calc_pss(f_s, N_ss):
    pss = f_s*(1-e**(-N_ss))
    return pss

# Probability of faculty infection in one class session: 
def calc_p1f(p_sf, N_s):
    p1f =1-(1-p_sf)**(N_s)
    return p1f

# Probability of student infection in one class session:
def calc_p1s(p_ss, n_s, p_fs, n_f):
    p1s = 1-((1-p_ss)**(n_s-1)*(1-p_fs)**n_f)
    return p1s

# Probability of faculty infection for semester:
def calc_pf(p1_f, n_c):
    pf = 1-(1-p1_f)**n_c
    return pf
    
# Probability of student infection for semester:
def calc_ps(p1_s, n_c):
    return 1
###



# original code
#%% Functions
def get_random(var,n=10000):
    return np.random.uniform(*var+[n])

def get_normal(var,n=10000):
    return np.random.normal(*var+[n])

def update_df(surface_area,
              height,
              num_faculty,
              num_students,
              duration,
              num_class_periods,
              breathing_rate_faculty,
              breathing_rate_student,
              ventilation_w_outside_air,
              decay_rate_of_virus,
              deposition_to_surface,
              additional_control_measures,
              quanta_emission_rate_faculty,
              quanta_emission_rate_student,
              exhalation_mask_efficiency,
              inhalation_mask_efficiency,
              background_infection_rate_faculty,
              background_infection_rate_student):
    #Create dataframe of 10,000 runs
    num_runs = 10000
    df = pd.DataFrame(index=np.arange(num_runs))
    df['VENT']  = get_random(ventilation_w_outside_air,num_runs)
    df['DECAY'] = get_random(decay_rate_of_virus,num_runs)
    df['DEP']   = get_random(deposition_to_surface,num_runs)
    df['OTHER'] = get_random(additional_control_measures,num_runs)
    df['L']     = df['VENT'] + df['DECAY'] + df['DEP'] + df['OTHER']
    df['LDUR']  = df['L'] * duration / 60
    df['VOL']   = surface_area * height*0.305**3
    df['EFFOUT'] = get_random(exhalation_mask_efficiency,num_runs)
    df['EMMFx']  = get_normal(quanta_emission_rate_faculty,num_runs)
    df['EMMSx']  = get_normal(quanta_emission_rate_student,num_runs)
    df['EMMF'] = 10**df['EMMFx']
    df['EMMS'] = 10**df['EMMSx']
    df['INFRATEF'] = get_random(background_infection_rate_faculty,num_runs)
    df['INFRATES'] = get_random(background_infection_rate_student,num_runs)
    df['CONCF'] = df['EMMF']*(1-df['EFFOUT'])/(df['L']*df['VOL'])*(1-1/df['LDUR']*(1-np.exp(-df['LDUR'])))
    df['CONCS'] = df['EMMS']*(1-df['EFFOUT'])/(df['L']*df['VOL'])*(1-1/df['LDUR']*(1-np.exp(-df['LDUR'])))
    df['EFFIN'] = get_random(inhalation_mask_efficiency,num_runs)
    df['BRFx']   = get_random(breathing_rate_faculty,num_runs)
    df['BRSx']   = get_random(breathing_rate_student,num_runs)
    df['BRF']   = 60 * df['BRFx']
    df['BRS']   = 60 * df['BRSx']
    df['INF_S'] = df['CONCS'] * df['BRF'] * duration/60 * (1-df['EFFIN'])
    df['INS_F'] = df['CONCF'] * df['BRS'] * duration/60 * (1-df['EFFIN'])
    df['INS_S'] = df['CONCS'] * df['BRS'] * duration/60 * (1-df['EFFIN']) 
    # INECTION PROBABILITIES FOR FACULTY/STUDENT INFECTION
    df['PF_S']  = df['INFRATES'] * (1 - np.exp(-df['INF_S']))
    df['PS_F']  = df['INFRATEF'] * (1 - np.exp(-df['INS_F']))
    df['PS_S']  = df['INFRATES'] * (1 - np.exp(-df['INS_S']))
    # INFECTION PROBABILITIES FOR 1 CLASS SESSION
    df['PF'] = 1 - ((1-df['PF_S'])**(num_students))
    df['PS'] = 1 - (((1-df['PS_S'])**(num_students-1))*((1-df['PS_F'])**(num_faculty)))
    # INFECTION PROBABILITIES FOR SEMESTER
    df['nPF'] = 1 - df['PF']
    df['nPFsemester'] = df['nPF']**num_class_periods
    df['PFsemester']  = 1 - df['nPFsemester']
    df['nPS'] = 1 - df['PS']
    df['nPSsemester'] = df['nPS']**num_class_periods
    df['PSsemester']  = 1 - df['nPSsemester']
    return(df)

def update_figure(df,faculty=True):
    if faculty: fld = 'PFsemester'; txt = 'Faculty'
    else: fld = 'PSsemester'; txt = 'Student'
    #Get the max x value
    # x_maxf = df['PFsemester'].max()
    # x_maxs = df['PSsemester'].max()
    x_maxf = df['PFsemester'].quantile(0.99)
    x_maxs = df['PSsemester'].quantile(0.99)
    x_max = max(x_maxf, x_maxs)
    #Update the figure
    fig = px.histogram(df,x=fld,nbins=40,histnorm='percent',
                       title=f'Calculated Distribution of {txt} Infection Probabilities for Semester<br>from 10,000 Monte Carlo Simulations')
    fig.update_xaxes(title_text = 'Probability of infection (%)',
                     range=[0,x_max])
    fig.update_yaxes(title_text = 'Percentage of 10,000 Monte Carlo cases')
    fig.update_layout(xaxis_tickformat = "%",
                      font_size=10)
    #fig.update_layout(transition_duration=500)
    return(fig)

def summarize_output(df,faculty=True):
    if faculty: fld = 'PFsemester'; txt = 'FOR FACULTY MEMBER TEACHING THE COURSE'
    else: fld = 'PSsemester'; txt = 'FOR A STUDENT TAKING THE COURSE'
    #Create markdown from values
    the_mean = df[fld].mean()
    the_quants = [df[fld].quantile(x) for x in (0.05,0.25,0.5,0.75,0.95)]
    #Create Markdown
    md_text=f'''  
**{txt}**
| Best Estimate of Infection Probability | {the_mean:0.2%} |
| --: | --- |
| 5% chance that infection probability will be less than | {the_quants[0]:0.2%} |
| 25% chance that infection probability will be less than | {the_quants[1]:0.2%} |
| 50% chance that infection probability will be less than | {the_quants[2]:0.2%} |
| 75% chance that infection probability will be less than | {the_quants[3]:0.2%} |
| 95% chance that infection probability will be less than | {the_quants[4]:0.2%} |
'''
    return md_text

def summarize_outputx(df,faculty=True):
    if faculty: fld = 'PFsemester'; txt = ''
    else: fld = 'PSsemester'; txt = ''
    #Create markdown from values
    the_mean = df[fld].mean()
    the_quants = [df[fld].quantile(x) for x in (0.05,0.25,0.5,0.75,0.95)]
    #Create Markdown
    md_text=f'''
'''
    return 

def update_results(first_click=False):
    if first_click:
        return '### Results will be displayed here'
    md_text = '''
    ### Predicted Infection Probabilities for the Semester
    '''
    return md_text

#%%Read in the static data
df = update_df()
fig = update_figure(df)
md_results = summarize_outputx(df)
