CXX      := g++
PYTHON   := python3

PY_INC   := $(shell $(PYTHON) -c "import pybind11; print(pybind11.get_include())" 2>/dev/null || echo "/usr/include/pybind11")
PY_FLAGS := $(shell $(PYTHON)-config --includes)
PY_LDFLAGS := $(shell $(PYTHON)-config --ldflags --embed 2>/dev/null || $(PYTHON)-config --ldflags)

# Check for MKL environment
ifneq ($(or $(PRELOAD_MKL),$(wildcard PRELOAD_MKL)),)
  BLAS_INC  := /usr/include/mkl
  BLAS_LIB  := -Wl,--no-as-needed -lmkl_rt -Wl,--as-needed
else
  BLAS_INC  := /usr/include/x86_64-linux-gnu
  BLAS_LIB  := -lopenblas
endif

EXT_SUFFIX := $(shell $(PYTHON)-config --extension-suffix)
TARGET     := _matrix$(EXT_SUFFIX)

CXXFLAGS := -O3 -march=native -std=c++17 -fPIC -I$(PY_INC) -I$(BLAS_INC)
LDFLAGS  := -shared $(PY_LDFLAGS) $(BLAS_LIB)

.PHONY: all test clean

all: $(TARGET)

$(TARGET): matrix.cpp
	$(CXX) $(CXXFLAGS) $(PY_FLAGS) $< $(LDFLAGS) -o $@

test: $(TARGET)
	$(PYTHON) -m pytest test_matrix.py -v

clean:
	rm -f $(TARGET) performance.txt
	rm -rf __pycache__ .pytest_cache
