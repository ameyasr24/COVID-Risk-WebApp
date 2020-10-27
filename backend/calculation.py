import numpy as np
import pandas as pd
import math
from getCountyCases import getCountyCases
import statistics

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
for x in range(trials):
    randomizeAll()
    cf = calc_Cf(quanta_emission_rate_faculty[2], exhalation_mask_efficiency[2], (ventilation_w_outside_air[2]+decay_rate_of_virus[2]+deposition_to_surface[2]+additional_control_measures[2]), duration)
    cs = calc_Cs(quanta_emission_rate_student[2], exhalation_mask_efficiency[2], (ventilation_w_outside_air[2]+decay_rate_of_virus[2]+deposition_to_surface[2]+additional_control_measures[2]), duration)
    Nfs = calc_Nfs(cf, background_infection_rate_student[2], inhalation_mask_efficiency[2], duration)
    Nsf = calc_Nsf(cs, background_infection_rate_student[2], inhalation_mask_efficiency[2], duration)
    Nss = calc_Nss(cs, background_infection_rate_student[2], inhalation_mask_efficiency[2], duration)
    Pfs = calc_pfs(percent_faculty_infectious[2], Nfs)
    Psf = calc_psf(percent_student_infectious[2], Nsf)
    Pss = calc_pss(percent_student_infectious[2], Nss)
    P1f = calc_p1f(Psf, num_students)
    P1s = calc_p1s(Pss, num_students, Pfs, num_faculty)
    Pf = calc_pf(P1f, num_class_periods)
    Ps = calc_ps(P1s, num_class_periods)
    fac_runs[x] = Pf
    student_runs[x] = Ps

student_mean = statistics.mean(student_runs)
fac_mean = statistics.mean(fac_runs)

student_quants_05 = np.quantile(student_runs, 0.05)
student_quants_25 = np.quantile(student_runs, 0.25)
student_quants_50 = np.quantile(student_runs, 0.50)
student_quants_75 = np.quantile(student_runs, 0.75)
student_quants_95 = np.quantile(student_runs, 0.95)

fac_quants_05 = np.quantile(student_runs, 0.05)
fac_quants_25 = np.quantile(student_runs, 0.25)
fac_quants_50 = np.quantile(student_runs, 0.50)
fac_quants_75 = np.quantile(student_runs, 0.75)
fac_quants_95 = np.quantile(student_runs, 0.95)

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
    ps = 1-(1-p1_s)**n_c
    return ps