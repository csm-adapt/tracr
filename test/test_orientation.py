import sys
sys.path.append('..')
from tracr.distribution.orientation import principal
from itertools import product, combinations
import numpy as np

# To test, simply run
# [...]$ nosetests (optionally with -v)
#and a report a summary of the results


class TestClass: # keep this the same
    def setUp(self):
        # construct objects and perform any necessary setup
        pass

    def test_principal(self):
        def handedness(arr):
            assert len(arr.shape) == 2
            assert arr.shape[0] == arr.shape[1]
            return np.sign(np.linalg.det(arr))
        def fix_signs(ref, change):
            # the direction of the basis vectors may not be the same, though
            # their magnitudes are comparable. This ensures the signs are
            # correct. This operation is done in place.
            ref = np.asarray(ref)
            change = np.asarray(change)
            assert ref.shape == change.shape
            assert len(ref.shape) == 2
            assert ref.shape[0] == ref.shape[1]
            signs = np.sign(ref/change)
            dim = ref.shape[0]
            for row in range(dim):
                if np.all(signs[row] < 0):
                    change[row] *= -1.0
                    signs[row] *= -1.0
            for col in range(dim):
                if np.all(signs[:,col] < 0):
                    change[:,col] *= -1.0
                    signs[:,col] *= -1.0
        # run test one
        imax, jmax, kmax = 128, 128, 128
        field = np.zeros((imax, jmax, kmax), dtype=bool)
        # create an axis-aligned ellipse
        xaxis = np.sqrt(imax-8)
        yaxis = np.sqrt(jmax-24)
        zaxis = np.sqrt(kmax-40)
        for i,j,k in product(xrange(imax), xrange(jmax), xrange(kmax)):
            r  = ((float(i)-imax//2)/xaxis)**2
            r += ((float(j)-jmax//2)/yaxis)**2
            r += ((float(k)-kmax//2)/zaxis)**2
            if r < 1:
                field[i,j,k] = True
        # randomly rotate the ellipse
        thetaPhiPsi = np.pi/2. * np.random.random(size=(3,))
        cq, cf, cs = np.cos(thetaPhiPsi)
        sq, sf, ss = np.sin(thetaPhiPsi)
        D = np.array([
            [ cf, sf,  0],
            [-sf, cf,  0],
            [  0,  0,  1]])
        C = np.array([
            [  1,  0,  0],
            [  0, cq, sq],
            [  0,-sq, cq]])
        B = np.array([
            [ cs, ss,  0],
            [-ss, cs,  0],
            [  0,  0,  1]])
        A = np.dot(B, np.dot(C, D))
        # check that the rotation matrix is orthonormal
        if not (np.all(np.isclose(np.linalg.norm(A, axis=0), np.ones(3))) and
                np.all(np.isclose(np.linalg.norm(A, axis=1), np.ones(3)))):
            raise ValueError("Rotation matrix for {} " \
                             "is not normal.".format(thetaPhiPsi))
        if not np.all([np.isclose(np.dot(A[i],A[j]), 0) for i,j in
                       combinations(range(3), 2)]):
            proj = ['{}: {}'.format((i,j), np.dot(A[i], A[j]))
                    for i,j in combinations(range(3), 2)]
            raise ValueError("Rotation matrix\n{}\nis " \
                             "not orthogonal.\n{}".format(A, proj))
        ## rotate the ellipse
        # from (xi, yi, zi) to ((x,y,z)_0, (x,y,z)_1,...)
        ijk = np.transpose(np.where(field))
        offset = np.mean(ijk, axis=0)
        ijk = ijk - offset
        # (DIM x DIM).(N x DIM)^T = (DIM x N) --> transpose --> (N x DIM)
        ijk = np.dot(A, ijk.T).T
        # reshift to new offset, store as int, transpose --> (DIM x N)
        ijk = tuple((offset + ijk).astype(int).T)
        field[:] = False # reset field to empty
        field[ijk] = True
        ## rotate the coordinate axes
        # check
        trueAxes = np.dot(A, np.eye(3)) # these should be the eigenvectors
        # calculated eigenvectors
        testAxes = principal(field)
        # fix the signs, which should also fix the handedness
        fix_signs(trueAxes, testAxes)
        # check
        proj = [np.max(np.abs(np.dot(vi, vj)), np.abs(np.dot(vi, -vj)))
                for vi,vj in zip(trueAxes, testAxes)]
        check = np.all([np.isclose(proj, 1.0, rtol=0.01)])
        #check = np.all(check)
        if not check:
            msg = [
                '',
                '{} !='.format(trueAxes),
                '{}'.format(testAxes),
                'Projections:']
            for p in proj:
                msg.append('  {}'.format(p))
            msg = '\n'.join(msg)
            assert False, msg
        else:
            return True

    def tearDown(self):
        # clean up
        pass
