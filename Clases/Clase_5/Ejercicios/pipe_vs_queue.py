from multiprocessing import Pipe, Queue

conn1, conn2 = Pipe()
conn1.send("Hola")
print(conn2.recv())


q = Queue()
q.put("Hola")
print(q.get())
