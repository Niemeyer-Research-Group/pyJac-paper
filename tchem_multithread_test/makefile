CC=gcc
CFLAGS=-O3 -g -std=c99 -fopenmp
#replace with correct path to TCHEM install
TC_HOME=$(TCHEM_HOME)
#set paths and libs
LDIR=$(TC_HOME)/lib
IDIR=$(TC_HOME)/include
LIBS=-ltchem -lm -fopenmp
CFLAGS += -I$(IDIR)

.PHONY: clean default
default: tctest
clean:
	@rm -f tctest *.o kmod.* math_* data.bin *.pyc

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

tctest: read_initial_conditions.o test.o mechanism.o mass_mole.o
	gcc -o $@ $^ -L$(LDIR) $(LIBS)
