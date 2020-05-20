#coding:utf-8
import sqlite3
import re
import queue

# import data from database.
def Getdata(q):
 db=sqlite3.connect("Dataset.db")
 cursor=db.cursor()
 cursor.execute("SELECT * FROM Tasks ORDER BY Arrival ASC")
 for i in cursor.fetchall():
   q.put(i) # store tasks in a queue.
 db.commit()
 db.close()

#ID Check;Separately create list tasks for next step.
def IDCheck(ID,Arrival,Duration):
 global clock
 count=0
 if clock ==Arrival:
  if re.search("[a-z]",ID):
   count +=1
  if re.search("[A-Z]",ID):
   count +=1 
  if re.search("[0-9]",ID):
   count +=1
  if re.search("[@+_+#+*+-+&]",ID):
   count +=1
  if count>=3:
   I.append(ID) #Task list: Accepted: I(ID),A(Arrival),D(Duration);
   A.append(Arrival)
   D.append(Duration)
  else :
   IDdis.append(ID) #Discarded: IDdis(IDDiscared),A(ArrivalDiscared),D(DurationDiscared).
   Adis.append(Arrival)
   Ddis.append(Duration)
 else: 
  clock =Arrival
  IDCheck(ID,Arrival,Duration)

#Assign tasks to a processor; all printing store in list Tasks
def Assign():
 k,j=0,0 # the count in the I[],A[],D[] and IDdis[],Adis[],Ddis[]
 for i in range(100): #update clock every loop.
  clock=Arrivals[i]
  if clock in A: #determine whether the clock is accepted.

#task1,2,3 are special, cannot be compared with privous three, 
#so coding is written for them separetely.
   try:
    if k==0: #the task1 is assigned to processor directly.
     Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
     Tasks.append(["**Task {} accepted".format (I[k]),clock])
     Tasks.append(["** {}: Task {} assigned to processor 1".format(clock,I[k]),clock])
     processor1.put_nowait(I[k])
     clock=A[k]+D[k]
     Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
     k=k+1

#the task2 is compared with task1's time: >=:assign to processor1; <:assign to processor2.
    elif k==1: 
     if A[k]>A[0]+D[0]:
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** {}: Task {} assigned to processor 1".format(clock,I[k]),clock])
      processor1.put_nowait(I[k])
      clock=A[k]+D[k]
      Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
     elif A[k]<A[0]+D[0]:
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** {}: Task {} assigned to processor 2".format(clock,I[k]),clock])
      processor2.put(I[k])
      clock=A[k]+D[k]
      Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
      k=k+1 
 
#the task3 is compared with task1,2's time: < both:assign to processor3; >:assign to min(processor1,2).
    elif k==2:
     if A[k]> A[0]+D[0] :
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** {}: Task {} assigned to processor 1".format(clock,I[k]),clock])
      processor1.put_nowait(I[k])
      clock=A[k]+D[k]
      Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
      k=k+1
     elif A[k]> A[1]+D[1] :
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** {}: Task {} assigned to processor 2".format(clock,I[k]),clock])
      processor2.put_nowait(I[k])
      clock=A[k]+D[k]
      Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
      k=k+1
     else:
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** {}: Task {} assigned to processor 3".format(clock,I[k]),clock])
      processor3.put_nowait(I[k])
      clock=A[k]+D[k]
      Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
      k=k+1

#from task4, tasks are compared with previous three.
    else:

#task'time(i) is large than any one, assign to min(Processor1,2,3).
     if A[k]> max(A[k-3]+D[k-3],A[k-2]+D[k-2],A[k-1]+D[k-1]):
      if A[k-3]+D[k-3]<min(A[k-2]+D[k-2],A[k-1]+D[k-1]):
       Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
       Tasks.append(["**Task {} accepted".format (I[k]),clock])
       Tasks.append(["** {}: Task {} assigned to processor 1".format(clock,I[k]),clock])
       processor1.put_nowait(I[k])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
       k=k+1
      elif A[k-2]+D[k-2]<min(A[k-3]+D[k-3],A[k-1]+D[k-1]):
       Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
       Tasks.append(["**Task {} accepted".format (I[k]),clock])
       Tasks.append(["** {}: Task {} assigned to processor 2".format(clock,I[k]),clock])
       processor2.put_nowait(I[k])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
       k=k+1
      else:
       Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
       Tasks.append(["**Task {} accepted".format (I[k]),clock])
       Tasks.append(["** {}: Task {} assigned to processor 3".format(clock,I[k]),clock])
       processor3.put_nowait(A[k])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k]),clock])
       k=k+1

#hold: when the task < all of the previous three.  
     elif A[k]< max(A[k-3]+D[k-3],A[k-2]+D[k-2],A[k-1]+D[k-1]):
      Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,I[k],D[k]),clock])
      Tasks.append(["**Task {} accepted".format (I[k]),clock])
      Tasks.append(["** Task {} on hold.".format(I[k]),clock])
#when one processor is available--clock==min(Processor's time).
      A[k]=min(A[k-3]+D[k-3], A[k-2]+D[k-2], A[k-1]+D[k-1])
      k=k+1
      if A[k-3]+D[k-3]<min(A[k-2]+D[k-2],A[k-1]+D[k-1]):  
       Tasks.append(["** {}: Task {} assigned to processor 1".format(clock,I[k-1]),clock])
       processor1.put_nowait(I[k-1])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k-1]),clock])
       k=k+1
      elif A[k-2]+D[k-2]<min(A[k-3]+D[k-3],A[k-1]+D[k-1]):
       Tasks.append(["** {}: Task {} assigned to processor 2".format(clock,I[k-1]),clock])
       processor2.put_nowait(I[k-1])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k-1]),clock])
       k=k+1
      else:
       Tasks.append(["** {}: Task {} assigned to processor 3".format(clock,I[k-1]),clock])
       processor3.put_nowait(I[k-1])
       clock=A[k]+D[k]
       Tasks.append(["** {} : Task {} completed.".format(clock,I[k-1]),clock])
       k=k+1
   except IndexError :
    continue
    
  elif clock in Adis: #determine whether the clock is discarded
   try:
    clock=Adis[j]
    Tasks.append(["** {}: Taks {} with duration {} enters the system".format(clock,IDdis[j],Ddis[j]),clock])
    Tasks.append(["**Task {} unfeasible and discarded".format (IDdis[0]),clock])
    IDdis.remove(IDdis[0]) # every loop, delete the first data
    j=j+1
   except IndexError :
    continue  
 

# Main
clock=float(0)
I,A,D=[],[],[] #Task list: Accepted: I(ID),A(Arrival),D(Duration); 
IDdis,Adis,Ddis=[],[],[] #Discarded: IDdis(IDDiscared),A(ArrivalDiscared).
Arrivals=[]
Tasks=[]
processor1=queue.Queue()
processor2=queue.Queue()
processor3=queue.Queue()
q=queue.Queue()

# import data from database; system initialised
Getdata(q)
print("** SYSTEM INITIALISED **")

#ID check; create list Arrivals for next step
for i in range(100):
 Task=q.get()
 IDCheck(Task[0],Task[1],Task[2])
 Arrivals.append(Task[1])

#Assign to a processor
Assign()

#display, by clock Ascending order
Tasks.sort(key=lambda l:l[-1])
for i in Tasks:
 print(i[0])


print ("** {}: SIMULATION COMPLETED. **".format(clock))
