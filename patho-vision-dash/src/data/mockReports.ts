import { DashboardReport } from '@/types/pathology';

/**
 * Mock reports for development/fallback mode
 * Use these when API is unavailable
 */
export const mockReports: DashboardReport[] = [
  {
    // Backend fields
    report_id: 'RPT-001',
    patient_id: 'patient_12345',
    pathologist_id: 'path_001',
    tissue_sample_id: 'colon_biopsy_001',
    diagnosis: 'precancerous',
    findings: 'High-grade dysplasia identified; Architectural distortion present; Nuclear atypia with loss of polarity; No invasive carcinoma detected',
    recommendations: 'Close clinical follow-up required; Consider repeat colonoscopy in 3-6 months; Discuss with GI oncology team',
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    raw_text: `SPECIMEN: Colon, sigmoid, biopsy

CLINICAL HISTORY: 58-year-old male with family history of colon cancer, screening colonoscopy.

GROSS DESCRIPTION: Received in formalin labeled with patient name and "sigmoid colon" are multiple fragments of tan-pink soft tissue measuring 0.3 x 0.2 x 0.1 cm in aggregate. Entirely submitted in one cassette.

MICROSCOPIC DESCRIPTION: Sections show colonic mucosa with architectural distortion and nuclear atypia consistent with high-grade dysplasia. The dysplastic epithelium shows loss of nuclear polarity, increased nuclear to cytoplasmic ratio, and hyperchromasia. No evidence of invasive carcinoma is identified in the sections examined.

DIAGNOSIS:
Sigmoid colon, biopsy:
- HIGH-GRADE DYSPLASIA
- No invasive carcinoma identified
- Recommend close clinical correlation and follow-up`,

    // Workflow state
    current_step: 'creating_clinical_plan',
    clinical_plan: {
      plan_id: 'plan_001',
      report_id: 'RPT-001',
      patient_id: 'patient_12345',
      clinician_id: 'clinician_001',
      diagnosis: 'precancerous',
      treatment_plan: `Based on the pathology findings of high-grade dysplasia in the sigmoid colon, I recommend the following management plan:

1. **Immediate Actions:**
   - Schedule follow-up colonoscopy in 3 months
   - Refer to GI oncology for evaluation
   - Consider genetic counseling given family history

2. **Monitoring:**
   - Close surveillance with repeat colonoscopy every 3-6 months initially
   - If stable, may extend to annual surveillance

3. **Patient Education:**
   - Discuss significance of high-grade dysplasia
   - Review family history and increased risk
   - Emphasize importance of compliance with surveillance

4. **Coordination:**
   - Send records to GI oncology
   - Coordinate with primary care for overall management
   - Ensure patient understands follow-up plan`,
      follow_up_actions: [
        'Schedule follow-up colonoscopy in 3 months',
        'Refer to GI oncology',
        'Genetic counseling consultation'
      ],
      urgency_level: 'urgent',
      created_at: new Date().toISOString(),
    },

    // UI fields
    patientName: 'John Doe',
    patientMRN: 'MRN-12345',
    patientDOB: '1965-03-15',
    category: 'Precancerous',
    status: 'plan_ready',
    priority: 'urgent',
    specimenType: 'Colon biopsy',
    receivedDate: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    structuredData: {
      findings: [
        'High-grade dysplasia identified',
        'Architectural distortion present',
        'Nuclear atypia with loss of polarity',
        'No invasive carcinoma detected'
      ],
      recommendations: [
        'Close clinical follow-up required',
        'Consider repeat colonoscopy in 3-6 months',
        'Discuss with GI oncology team',
        'Genetic counseling may be appropriate given family history'
      ]
    },
    clinicalPlanText: `Based on the pathology findings of high-grade dysplasia in the sigmoid colon, I recommend the following management plan:

1. **Immediate Actions:**
   - Schedule follow-up colonoscopy in 3 months
   - Refer to GI oncology for evaluation
   - Consider genetic counseling given family history

2. **Monitoring:**
   - Close surveillance with repeat colonoscopy every 3-6 months initially
   - If stable, may extend to annual surveillance

3. **Patient Education:**
   - Discuss significance of high-grade dysplasia
   - Review family history and increased risk
   - Emphasize importance of compliance with surveillance

4. **Coordination:**
   - Send records to GI oncology
   - Coordinate with primary care for overall management
   - Ensure patient understands follow-up plan`,
    patientMessageText: `Dear Mr. Doe,

Your recent colon biopsy results are ready. The test found abnormal cells called "high-grade dysplasia." While these cells are not cancer, they are considered precancerous and require close monitoring.

What this means:
- These abnormal cells have the potential to develop into cancer if not monitored
- This is a treatable condition when caught early
- Your doctor will create a surveillance plan for you

Next steps:
- We will schedule a follow-up colonoscopy in 3 months
- You will also be referred to a specialist in gastrointestinal oncology
- Given your family history, genetic counseling may be recommended

Please contact your doctor's office to schedule these appointments. It's important to follow the recommended surveillance plan closely.

If you have any questions or concerns, please don't hesitate to reach out to your care team.

Best regards,
Your Care Team`
  },
  {
    // Backend fields
    report_id: 'RPT-002',
    patient_id: 'patient_67890',
    pathologist_id: 'path_002',
    tissue_sample_id: 'skin_biopsy_002',
    diagnosis: 'benign',
    findings: 'Compound melanocytic nevus identified; Mild architectural disorder present; Focal cytologic atypia noted; No evidence of melanoma; Lesion completely excised',
    recommendations: 'Routine skin surveillance; Annual full body skin examination; Patient education on self-examination',
    created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    raw_text: `SPECIMEN: Skin, left shoulder, shave biopsy

CLINICAL HISTORY: 52-year-old female, changing mole on left shoulder.

DIAGNOSIS:
Skin, left shoulder, shave biopsy:
- BENIGN COMPOUND MELANOCYTIC NEVUS with mild atypia (dysplastic nevus)
- Lesion appears completely excised
- No evidence of melanoma`,

    // Workflow state
    current_step: 'completed',

    // UI fields
    patientName: 'Sarah Miller',
    patientMRN: 'MRN-67890',
    patientDOB: '1972-08-22',
    category: 'Normal',
    status: 'completed',
    priority: 'routine',
    specimenType: 'Skin lesion, left shoulder',
    receivedDate: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    structuredData: {
      findings: [
        'Compound melanocytic nevus identified',
        'Mild architectural disorder present',
        'Focal cytologic atypia noted',
        'No evidence of melanoma',
        'Lesion completely excised'
      ],
      recommendations: [
        'Routine skin surveillance',
        'Annual full body skin examination',
        'Patient education on self-examination',
        'Sun protection counseling'
      ]
    },
  },
  {
    // Backend fields
    report_id: 'RPT-003',
    patient_id: 'patient_54321',
    pathologist_id: 'path_003',
    tissue_sample_id: 'thyroid_fna_003',
    diagnosis: 'benign',
    findings: 'Benign follicular cells present; Abundant colloid noted; No suspicious features identified',
    recommendations: 'Routine clinical follow-up; Repeat ultrasound in 12-24 months',
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    raw_text: `SPECIMEN: Thyroid, right lobe, fine needle aspiration

CLINICAL HISTORY: 44-year-old male with palpable right thyroid nodule.

DIAGNOSIS: Bethesda Category II - BENIGN
- Consistent with benign follicular nodule (adenomatoid nodule/colloid nodule)`,

    // Workflow state
    current_step: 'completed',

    // UI fields
    patientName: 'Michael Chen',
    patientMRN: 'MRN-54321',
    patientDOB: '1980-11-30',
    category: 'Normal',
    status: 'completed',
    priority: 'routine',
    specimenType: 'Thyroid FNA',
    receivedDate: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    structuredData: {
      findings: [
        'Benign follicular cells present',
        'Abundant colloid noted',
        'No suspicious features identified',
        'Adequate sample for evaluation'
      ],
      recommendations: [
        'Routine clinical follow-up',
        'Repeat ultrasound in 12-24 months',
        'No immediate intervention required'
      ]
    },
  },
  {
    // Backend fields
    report_id: 'RPT-004',
    patient_id: 'patient_98765',
    pathologist_id: 'path_004',
    tissue_sample_id: 'breast_biopsy_004',
    diagnosis: 'inconclusive',
    findings: 'Sample processing in progress',
    created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    raw_text: 'Report is being processed by AI agent...',

    // Workflow state
    current_step: 'processing_report',

    // UI fields
    patientName: 'Emily Rodriguez',
    patientMRN: 'MRN-98765',
    patientDOB: '1955-05-18',
    category: 'Abnormal',
    status: 'analyzing',
    priority: 'stat',
    specimenType: 'Breast core biopsy',
    receivedDate: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
  }
];
