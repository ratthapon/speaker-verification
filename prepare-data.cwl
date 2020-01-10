class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: prepare_data
baseCommand:
  - python3
inputs:
  - id: projectDirectory
    type: Directory?
  - id: trainingSet
    type: File?
    inputBinding:
      position: 0
      prefix: '--training-set'
  - id: testingSet
    type: File?
    inputBinding:
      position: 0
      prefix: '--testing-set'
  - id: wavDirectory
    type: Directory?
    inputBinding:
      position: 0
      prefix: '--wav-dir'
  - id: splitRatio
    type: float?
    inputBinding:
      position: 0
      prefix: '--ratio'
outputs:
  - id: outTrainingSet
    type: File?
    outputBinding:
      glob: $(inputs.trainingSet.path)
  - id: outTestingSet
    type: File?
    outputBinding:
      glob: $(inputs.trainingSet.path)
label: Prepare Data
arguments:
  - position: 0
    prefix: ''
    separate: false
    valueFrom: $(inputs.projectDirectory.path)/prepareTIMITSampleDataset.py
  - position: 0
requirements:
  - class: ResourceRequirement
    coresMin: 1
  - class: InlineJavascriptRequirement
