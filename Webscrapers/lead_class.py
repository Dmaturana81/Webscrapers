#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 10:10:03 2017

@author: matu
"""

class lead:
    """A class for lead to be filled with information from websites and easily exported to excel for Salesforce"""
    
    #Defining attributes of lead class present in SF


    title = ''
    position = ''
    description = ''
    city = ''
    CEP = ''
    institute = ''
    institution = ''
    email_s = ''
    phone = ''
    name = ''
    interest = ''
    street = ''
    
    def __init__(self, company, country, state, url, email=None, f_name=None, l_name=None,
                 affiliation = 'Academia' ,source = 'Sales', source_det = 'Data Mining',
                 status = 'Open', name=None, phone = None, position =None, c_website=None, desc = None, CEP = None ):
        self.company = company
        self.country = country
        self.state = state
        self.url = url
        self.CEP = CEP
        if name is not None:
            self.name = name
            (self.f_name, self.l_name) = name.split(' ',1)
        else:
            self.name = ' '.join([f_name, l_name])
            self.f_name = f_name
            self.l_name = l_name
        if position is None:
            self.position = ''
        self.email = email
        self.affiliation = affiliation
        self.source = source
        self.source_det = source_det
        self.status = status
        self.C_website = c_website
        self.phone = phone
        self.description = desc

    
    def to_dict(self):
        dic = {'title':self.title,              'f_name':self.f_name,       'l_name':self.l_name,
               'institution':self.institution,  'institute':self.institute, 'company':self.company,
               'email':self.email,              'email_s':self.email_s,     'phone':self.phone,
               'position':self.position,        'C_website':self.url,       'status':self.status, 
               'description':self.description,  'name':self.name,           'source':self.source,
               'source_det':self.source_det,    'city':self.city,           'country':self.country,
               'state':self.state,              'CEP':self.CEP,             'interest':self.interest,
               }
        
        return dic
    
    def to_print(self):
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s' % (self.name, self.email, self.C_website, self.phone, self.company, self.CEP, self.description))



        
        
        
   # def export(self, ):
        
    
    
        
    