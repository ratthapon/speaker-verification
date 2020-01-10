class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: feature_extraction
baseCommand:
  - python3
inputs:
  - id: projectDirectory
    type: Directory?
  - id: dataset
    type: File?
    inputBinding:
      position: 0
      prefix: '--dataset'
  - id: featureSet
    type: File?
    inputBinding:
      position: 0
      prefix: '--feature-set'
  - id: model
    type: File?
    inputBinding:
      position: 0
      prefix: '--model'
outputs:
  - id: outFeatureSet
    type: File?
    outputBinding:
      glob: $(inputs.featureSet.path)
label: Feature Extraction
arguments:
  - position: 0
    prefix: ''
    separate: false
    valueFrom: $(inputs.projectDirectory.path)/FeatureExtraction.py
requirements:
  - class: ResourceRequirement
    coresMin: 1
  - class: InlineJavascriptRequirement
