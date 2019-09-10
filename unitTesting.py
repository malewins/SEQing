#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for SEQing"""
import unittest
import dashboard_binding_sites as db

class TestDashboard(unittest.TestCase):
    def testFormatChangeiCLIP(self):
        self.maxDiff = None
        null = None
        for test in ['svg', 'png']:
            self.assertEqual(eval(db.changeFormatiCLIP(test)), 
                {'response': {'props': {'config':{'toImageButtonOptions' : {'filename' : 'iCLIP', 'width' : None,
                'scale' : 1.0, 'height' : None, 'format' : test} }}}})
  
    def testFormatChangeRNA(self):
        self.maxDiff = None
        null = None
        for test in ['svg', 'png']:
            self.assertEqual(eval(db.changeFormatRNA(test)), 
                {'response': {'props': {'config':{'toImageButtonOptions' : {'filename' : 'RNA', 'width' : None,
                'scale' : 1.0, 'height' : None, 'format' : test} }}}})
    
    def testChangeLegendSpacing(self):
        self.maxDiff = None
        for test in [0, 0.1, 0.2, 0.3]:
            self. assertEqual(eval(db.changeLegendSpacing(test)),  {'response': {'props': {'children':str(test)}}} )
    
    def testShowHelpPopup(self):
        self.maxDiff = None
        null = None
        testVals = [((0,1),{'response': {'props': {'style': {"display": "none"}}}}),
                    ((1,0),{'response': {'props': {'style': {"display": "block"}}}}),
                    ((1,1),{'response': {'props': {'style': {"display": "none"}}}})]
        for test in testVals:
            self.assertEqual(eval(db.showHelpPopup(test[0][0],test[0][1])),test[1])
    
    def testPreviewColorEvent(self):
        self.maxDiff = None
        self.assertEqual(eval(db.previewColorEvent(23, None, 66)),
            {'response': {'props': {'style': {'backgroundColor': 'rgb(255, 255, 255)', 'color': 'rgb(255, 255, 255)'}}}})
        self.assertEqual(eval(db.previewColorEvent(23, 48, 66)), 
            {'response': {'props': {'style': {'backgroundColor': 'rgb(23,48,66)', 'color': 'rgb(23,48,66)'}}}})
        
    def testOverlap(self):
        self.assertTrue(db.overlap((1,4),(2,7)))
        self.assertTrue(db.overlap((1,4),(1,4)))
        self.assertFalse(db.overlap((1,4),(1,1)))
        self.assertFalse(db.overlap((1,4),(5,7)))
        self.assertFalse(db.overlap((1,4),(4,7)))
        
if __name__ == '__main__':
    unittest.main()