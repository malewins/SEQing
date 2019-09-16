#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for SEQing"""
import unittest
import dashboard_binding_sites as db
import json
import dash_html_components as html

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
            
    def testConirmColor(self):
        testCases = []
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' : 'rgb(23, 23, 23)'}, (23,23,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'} , (None,23,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}, (23,None,23)))
        testCases.append(('test', json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}, (23,23,None)))
        testCases.append(('set2', json.dumps({'set2' :'rgb(0,0,0)'}), {'set2' : 'rgb(244, 23, 23)'}, (244,23,23)))
        for i in testCases:
            self.assertEqual(eval(db.confirmColor(0, i[3][0], i[3][1], i[3][2], i[0], i[1])),{'response': {'props': {'children' : json.dumps(i[2])}}} ) 
    
    def testChangeColor(self):
        testCases = []
        testCases.append(('test',(22,34,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(22, 34, 134)'}))
        testCases.append(('test',(22,None,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        testCases.append(('test',(None,34,134), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        testCases.append(('test',(22,34,None), json.dumps({'test' :'rgb(0,0,0)'}), {'test' :'rgb(0,0,0)'}))
        for i in testCases:
            self.assertEqual(eval(db.changeColor(i[1][0], i[1][1], i[1][2], i[0], i[2])),{'response': {'props': {'children' : json.dumps(i[3])}}})
    
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
    
    def testCreateDetailRow(self):
        testCases = []
        tableColors = ['rgb(0,0,0)', 'rgb(1,1,1)']
        testCases.append(('attribute', 'data', 1,  html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                     html.Td(html.Table(children=
                                                        html.Tr(html.Td('attribute'.strip()))))],
                           style={'background-color': 'rgb(1,1,1)'}), None))
        testCases.append(('1;2;3;4;5;6', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td('5'.strip())),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))
        testCases.append(('1;2;3;4;?5;6', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td(html.A('?5'[1:], href = '?5'[1:].strip(), target = '_blank'))),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))
        falseCases = []
        falseCases.append(('1;2;3;4;?5;', 'data', 2,  
                          html.Tr(children=[html.Td(html.B('data'.replace('_', ' ').title())),
                                    html.Td(html.Details(title = str(6) + ' values', 
                                        children = [
                                            html.Summary(str(6) + ' values'), 
                                            html.Table(children = 
                                                [
                                                    html.Tr(html.Td('1'.strip())),
                                                    html.Tr(html.Td('2'.strip())),
                                                    html.Tr(html.Td('3'.strip())),
                                                    html.Tr(html.Td('4'.strip())),
                                                    html.Tr(html.Td(html.A('?5'[1:], href = '?5'[1:].strip(), target = '_blank'))),
                                                    html.Tr(html.Td('6'.strip()))
                                                ]
                                            )
                                        ]
                                    ))], style={'background-color': 'rgb(0,0,0)'}), 
                            None))                          
        for i in testCases:
            db.subTables = i[4]
            db.tableColors = tableColors
            self.assertEqual(db.createDetailRow(i[0], i[1], i[2]), i[3])
        for i in falseCases:
            db.subTables = i[4]
            db.tableColors = tableColors
            self.assertIsNot(db.createDetailRow(i[0], i[1], i[2]), i[3])
            
    def testCalculateBlocks(self):
        testCases = []
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,100, 20, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([30],[0.4],[21])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 20, 40, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([30],[0.2],[21])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (0,10, 5, 15, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([7,12],[0.4,0.2],[5,5])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 0, 10, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2,7],[0.2,0.4],[5,5])
        testCases.append((caseInput,caseOutput))
        # thickStart, thickEnd, blockStart, blockEnd, blockHeight
        caseInput = (5,15, 1, 11, 0.4)
        # blockVals, blockYs, blockWidths
        caseOutput = ([2.5,7.5],[0.2,0.4],[4,6])
        testCases.append((caseInput,caseOutput))
        for i in testCases:
            inputBlockVals = []
            inputBlockYs = []
            inputBlockWidths = []
            db.calculateBlocks(i[0][0],i[0][1],i[0][2],i[0][3], inputBlockVals, inputBlockWidths, inputBlockYs, i[0][4])
            output = (inputBlockVals, inputBlockYs, inputBlockWidths)
            print(output)
            self.assertCountEqual(output, i[1])
            
if __name__ == '__main__':
    unittest.main()