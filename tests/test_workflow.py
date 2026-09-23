"""Scientific invariants: sample boundaries, missingness, and survey domains."""
import sys
import unittest
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from stunting_data import prepare_frame, classify, IMPROVED_WATER, UNIMPROVED_WATER
spec=importlib.util.spec_from_file_location('desc',Path(__file__).resolve().parents[1]/'src/02_descriptive_analysis.py')
desc=importlib.util.module_from_spec(spec);spec.loader.exec_module(desc)

class Invariants(unittest.TestCase):
    def test_sample_and_missingness(self):
        n=8
        d=pd.DataFrame(dict(hv022=['a']*n,hv021=range(n),hv001=range(n),hv002=[1]*n,hvidx=[1]*n,
            hv103=['yes']*7+['no'],hc1=[0,59,60,10,10,10,10,10],
            hc70=[-200,-201,-300,-601,601,-600,600,-300],hv005=[1000000]*n,
            hc61=[None]*n,hv201=['sachet water']*n,hv205=['no facility/bush/field']*n))
        out,frame=prepare_frame(d)
        self.assertEqual(out.hv001.tolist(),[0,1,5,6])
        self.assertEqual(out.stunted.tolist(),[0,1,1,0])
        self.assertTrue(out.maternal_education.isna().all())
        self.assertEqual(len(frame),8)
    def test_unknown_water_is_not_silently_unimproved(self):
        with self.assertRaises(ValueError):classify(pd.Series(['unexpected'],name='hv201'),IMPROVED_WATER,UNIMPROVED_WATER)
        x=classify(pd.Series([None,'sachet water'],name='hv201'),IMPROVED_WATER,UNIMPROVED_WATER)
        self.assertTrue(pd.isna(x.iloc[0]));self.assertEqual(x.iloc[1],0)
    def test_domain_keeps_zero_contributing_psus(self):
        d=pd.DataFrame(dict(stratum=['a','a'],psu=[1,2],weight=[1.,1.],stunted=[0,1]))
        frame=pd.DataFrame(dict(stratum=['a']*3,psu=[1,2,3]))
        est,se,_,_=desc.taylor_ratio(d,frame,np.ones(2,bool))
        self.assertEqual(est,.5)
        self.assertAlmostEqual(se,np.sqrt(1.5*.5/4))

class PredictiveMath(unittest.TestCase):
    def test_predictor_preserves_nested_indices(self):
        from bayesian_workflow import linear_predictor
        X=np.array([[1.],[2.],[3.]])
        actual=linear_predictor(np.array([1.]),np.array([[2.]]),np.array([.5]),
            np.array([[2.,4.]]),X,np.array([0,0,1]),np.array([2.]),np.array([[1.,3.]]),np.array([0,0,1]))
        np.testing.assert_allclose(actual,[[6.,8.,15.]])
    def test_loglik_matches_bernoulli(self):
        from bayesian_workflow import bernoulli_loglik
        from scipy.special import expit
        from scipy.stats import bernoulli
        eta=np.array([[-3.,0.,4.],[2.,-1.,.5]])
        y=np.array([0,1,1])
        np.testing.assert_allclose(bernoulli_loglik(eta,y),bernoulli.logpmf(y,expit(eta)),rtol=1e-12)
        self.assertTrue(np.isfinite(bernoulli_loglik(np.array([[-1000.,1000.]]),np.array([0,1]))).all())

if __name__=='__main__':unittest.main()
