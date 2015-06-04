#!/usr/bin/env python
########################
# author: Nobuo Sato
# email : nsato@jlab.org
########################
import sys,os
import numpy as np
import pylab as py
import gzip

# tools for lhe data

class VEC4(object):
 
  def __init__(self,P):
    self.P=np.copy(P)
    self.hel=None  

  def __add__(self,other):
    return VEC4(self.P+other.P)

  def __sub__(self,other):
    return VEC4(self.P-other.P)

  def __eq__(self,other):
    return VEC4(self.P)

  def __mul__(self,other):
    if isinstance(other,VEC4):
      return self.dot4(self.P,other.P)
    else:
      return VEC4(self.P*other)

  def __rmul__(self,other):
    if isinstance(other,VEC4):
      return self.dot4(self.P,other.P)
    else:
      return VEC4(self.P*other)

  def __str__(self):
    P=self.P
    return '%0.5e, %0.5e, %0.5e, %0.5e'%(P[0],P[1],P[2],P[3])

  def dot4(self,A,B):
    return A[0]*B[0] - np.dot(A[1:],B[1:]) 

class EVENTS(object):

  def __init__(self,fname=None):

    self.fname=fname
    self.load_file()
    self.get_events()
    self.D={}

  def load_file(self):
    try:
      F=gzip.open(self.fname, 'rb')
      self.lhe=F.readlines()
      F.close()  
    except:
      print 'ERR: fname does not exist  :('

  def get_raw_events(self): 
    lhe=self.lhe
    EVENTS=[]
    cnt=-1
    while 1:
      cnt+=1
      if cnt==len(lhe): break
      if lhe[cnt].startswith('<event>'):
        EVENT=[]
        while 1:
          cnt+=1
          if lhe[cnt].startswith('</event>'): break
          EVENT.append(lhe[cnt])    
        #--additional filters
        EVENT=[e for e in EVENT if e.startswith('#')==False]
        EVENT=[e for e in EVENT if e.startswith('<')==False]
        EVENTS.append(EVENT)  
    return EVENTS

  def get_events(self):

    RAW_EVENTS=self.get_raw_events()
  
    EVENTS=[]
    for RE in RAW_EVENTS:
  
      PARTICLES=[]
      for line in RE[1:]: 
        l=line.split()

        ### filterout initiali state momenta
        #if int(l[1])=-1: continue 

        # construc dictionary for particle
        particle={}
        particle['pid']=int(l[0])
        particle['mass']  =float(l[10])
        particle['mom']   =np.zeros(4)
        particle['mom'][0]  =float(l[9])
        particle['mom'][1:4]=[float(x) for x in l[6:9]]
        particle['mom'] =VEC4(particle['mom'])

        PARTICLES.append(particle)

      EVENTS.append(PARTICLES)  

    self.EVENTS=EVENTS
    self.nevents=len(EVENTS)

# misc

def checkdir(path):
  if not os.path.exists(path): 
    os.makedirs(path)

def tex(x):
  return r'$\mathrm{'+x+'}$'

def save(data,name):  
  f=open(name,"w")
  cPickle.dump(data, f)
  f.close()

def load(name):  
  f=open(name,"r")
  data=cPickle.load(f)
  f.close()
  return data

def fill_between(x, y1, y2=0, ax=None, **kwargs):
  """Plot filled region between `y1` and `y2`.
  This function works exactly the same as matplotlib's fill_between, except
  that it also plots a proxy artist (specifically, a rectangle of 0 size)
  so that it can be added it appears on a legend.
  """
  ax = ax if ax is not None else py.gca()
  ax.fill_between(x, y1, y2, **kwargs)
  if kwargs['facecolor']=='none': kwargs['facecolor']='w'
  p = py.Rectangle((0, 0), 0, 0, **kwargs)
  ax.add_patch(p)
  return p

def plot_hist(ax,color,X,Y,label='',symbol='-'):
  """
  simple histogram routine
  """
  XX,YY=[],[]
  #XX.append(X[0])
  #YY.append(0)
  for i in range(len(Y)):
    XX.append(X[i])
    YY.append(Y[i])
    XX.append(X[i+1])
    YY.append(Y[i])
  #XX.append(X[len(X)-1])
  #YY.append(0)
  ax.plot(XX,YY,color+symbol,label=label)
  return XX,YY





