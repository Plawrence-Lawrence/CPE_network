driver: driver.cpp BankManager.o Event.o ArrayPriorityQueue.h ArrayQueue.h
	g++ driver.cpp BankManager.o Event.o -o test

BankManager.o: BankManager.h BankManager.cpp Event.o
	g++ -c BankManager.cpp

Event.o: Event.h Event.cpp
	g++ -c Event.cpp

clean:
	rm *.o driver
