class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: prepare_data
baseCommand:
  - python3
inputs:
  - id: projectDir
    type: Directory?
    inputBinding:
      position: 0
      prefix: '--outdir'
outputs:
  - id: trainingSet
    type:
      - File
      - type: array
        items: File
    outputBinding:
      glob: $(inputs.projectDir.path)/cfg/enroll_list_timit.csv
label: Prepare Data
arguments:
  - position: 0
    prefix: ''
    separate: false
    valueFrom: $(inputs.projectDir.path)/prepareTIMITSampleDataset.py
  - position: 0
requirements:
  - class: ResourceRequirement
    coresMin: 1
  - class: InlineJavascriptRequirement
