VERSION ?= v0.1
CC ?= gcc
CFLAGS ?= -O3 -Wall -Wextra -std=c11 -fomit-frame-pointer
ifeq ($(OS),Windows_NT)
  BIN := shear_cminer.exe
  LIBS ?= -lws2_32 -pthread
else
  BIN := shear_cminer_lin
  LIBS ?= -pthread
endif
SCALAR_OBJS := src/shear_miner.o src/shear_hash.o src/sha256.o src/sha256_dispatch.o
UNAME_M := $(shell uname -m)
ifeq ($(UNAME_M),arm64)
  ISA_OBJS := src/sha256_isa_stub.o
else ifeq ($(UNAME_M),aarch64)
  ISA_OBJS := src/sha256_isa_stub.o
else
  ISA_OBJS := src/sha256_ni.o
endif
.PHONY: all clean selftest
all: $(BIN)
src/shear_miner.o: src/shear_miner.c src/shear_miner_p1.inc src/shear_miner_p2.inc src/shear_miner_p3.inc src/shear_hash.h
	$(CC) $(CFLAGS) -c -o $@ src/shear_miner.c
src/%.o: src/%.c
	$(CC) $(CFLAGS) -c -o $@ $<
src/sha256_ni.o: src/sha256_ni.c src/sha256.h
	$(CC) $(CFLAGS) -msse4.1 -msha -c -o $@ src/sha256_ni.c
$(BIN): $(SCALAR_OBJS) $(ISA_OBJS)
	$(CC) $(CFLAGS) -o $@ $(SCALAR_OBJS) $(ISA_OBJS) $(LIBS)
selftest: $(BIN)
	./$(BIN) --selftest
clean:
	rm -f $(BIN) src/*.o
