import os

basePath = '/home/orthogonalstar/PythonProjects/Tak/'

os.system('pytest ' + basePath + 'testBasics.py')
os.system('pytest ' + basePath + 'testRoadCondition.py')
os.system('pytest ' + basePath + 'testEndCondition.py')
