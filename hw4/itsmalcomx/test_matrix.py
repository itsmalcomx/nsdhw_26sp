import pytest
import _matrix
import gc

def make_matrices(size):
    mat1 = _matrix.Matrix(size, size)
    mat2 = _matrix.Matrix(size, size)
    mat3 = _matrix.Matrix(size, size)
    for it in range(size):
        for jt in range(size):
            mat1[it, jt] = it * size + jt + 1
            mat2[it, jt] = it * size + jt + 1
            mat3[it, jt] = 0
    return mat1, mat2, mat3

class TestMatrix:
    def test_basic(self):
        size = 100
        mat1, mat2, mat3 = make_matrices(size)
        assert mat1.nrow == size
        assert mat1.ncol == size
        assert mat1[0, 1] == 2
        assert mat1 == mat2
        # Clean up explicitly to help tracker tests
        del mat1, mat2, mat3
        gc.collect()

    def test_shape(self):
        M = _matrix.Matrix(4, 7)
        assert M.nrow == 4
        assert M.ncol == 7

class TestNaive:
    def test_match_mkl(self):
        size = 100
        mat1, mat2, _ = make_matrices(size)
        ret_naive = _matrix.multiply_naive(mat1, mat2)
        ret_mkl   = _matrix.multiply_mkl(mat1, mat2)
        assert ret_naive.nrow == size
        assert ret_naive == ret_mkl

class TestTile:
    @pytest.mark.parametrize("tsize", [16, 32, 64])
    def test_match_mkl(self, tsize):
        size = 64
        mat1, mat2, _ = make_matrices(size)
        ret_tile = _matrix.multiply_tile(mat1, mat2, tsize)
        ret_mkl  = _matrix.multiply_mkl(mat1, mat2)
        assert ret_tile == ret_mkl
