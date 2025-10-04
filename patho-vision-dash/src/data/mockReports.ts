import { PathologyReport } from '@/types/pathology';

export const mockReports: PathologyReport[] = [
  {
    id: 'RPT-001',
    patientName: 'John Doe',
    patientMRN: 'MRN-12345',
    patientDOB: '1965-03-15',
    diagnosis: 'High-grade dysplasia',
    category: 'Precancerous',
    receivedDate: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    status: 'plan_ready',
    priority: 'urgent',
    specimenType: 'Colon biopsy',
    rawReport: `SPECIMEN: Colon, sigmoid, biopsy
    
CLINICAL HISTORY: 58-year-old male with family history of colon cancer, screening colonoscopy.

GROSS DESCRIPTION: Received in formalin labeled with patient name and "sigmoid colon" are multiple fragments of tan-pink soft tissue measuring 0.3 x 0.2 x 0.1 cm in aggregate. Entirely submitted in one cassette.

MICROSCOPIC DESCRIPTION: Sections show colonic mucosa with architectural distortion and nuclear atypia consistent with high-grade dysplasia. The dysplastic epithelium shows loss of nuclear polarity, increased nuclear to cytoplasmic ratio, and hyperchromasia. No evidence of invasive carcinoma is identified in the sections examined.

DIAGNOSIS: 
Sigmoid colon, biopsy:
- HIGH-GRADE DYSPLASIA
- No invasive carcinoma identified
- Recommend close clinical correlation and follow-up`,
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
    clinicalPlan: `Based on the pathology findings of high-grade dysplasia in the sigmoid colon, I recommend the following management plan:

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
    patientMessage: `Dear Mr. Doe,

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
    id: 'RPT-002',
    patientName: 'Sarah Miller',
    patientMRN: 'MRN-67890',
    patientDOB: '1972-08-22',
    diagnosis: 'Benign nevus with mild atypia',
    category: 'Abnormal',
    receivedDate: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    status: 'message_sent',
    priority: 'routine',
    specimenType: 'Skin lesion, left shoulder',
    rawReport: `SPECIMEN: Skin, left shoulder, shave biopsy

CLINICAL HISTORY: 52-year-old female, changing mole on left shoulder.

GROSS DESCRIPTION: Received in formalin is an ellipse of tan-brown skin measuring 0.8 x 0.6 x 0.2 cm. The specimen is serially sectioned and entirely submitted.

MICROSCOPIC DESCRIPTION: Sections show a compound melanocytic nevus with some architectural disorder and focal cytologic atypia. The nevus is well-circumscribed with nests of melanocytes at the dermal-epidermal junction and in the superficial dermis. There is mild variation in nest size and spacing. No significant pagetoid spread, severe cytologic atypia, or mitotic activity is identified.

DIAGNOSIS:
Skin, left shoulder, shave biopsy:
- BENIGN COMPOUND MELANOCYTIC NEVUS with mild atypia (dysplastic nevus)
- Lesion appears completely excised
- No evidence of melanoma`,
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
    clinicalPlan: `The biopsy shows a benign mole with some minor irregularities but no signs of skin cancer. The concerning lesion has been completely removed.

**Recommended Plan:**
1. No additional treatment needed at this time
2. Annual full body skin exam with dermatology
3. Monthly self-skin examinations
4. Sun protection measures (SPF 30+, protective clothing)
5. Report any new or changing lesions promptly`,
    patientMessage: `Dear Ms. Miller,

Good news! Your skin biopsy results show a benign (non-cancerous) mole with some minor irregularities. The concerning spot on your left shoulder has been completely removed during the biopsy.

What this means:
- No cancer was found
- The irregular mole has been fully removed
- No additional treatment is needed right now

Next steps:
- Continue with annual skin checks with your dermatologist
- Perform monthly self-examinations at home
- Use sun protection (SPF 30+ sunscreen, protective clothing)
- Let us know promptly if you notice any new or changing spots

We'll schedule your next annual skin exam in about 12 months. Please call if you have any questions or concerns.

Best regards,
Your Dermatology Team`
  },
  {
    id: 'RPT-003',
    patientName: 'Michael Chen',
    patientMRN: 'MRN-54321',
    patientDOB: '1980-11-30',
    diagnosis: 'No significant abnormality',
    category: 'Normal',
    receivedDate: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    status: 'completed',
    priority: 'routine',
    specimenType: 'Thyroid FNA',
    rawReport: `SPECIMEN: Thyroid, right lobe, fine needle aspiration

CLINICAL HISTORY: 44-year-old male with palpable right thyroid nodule.

ADEQUACY: Adequate for evaluation (>6 groups of well-preserved follicular cells)

DIAGNOSIS: Bethesda Category II - BENIGN
- Consistent with benign follicular nodule (adenomatoid nodule/colloid nodule)

INTERPRETATION: The aspirate shows abundant colloid with scattered benign-appearing follicular cells in sheets and small groups. No features suspicious for malignancy are identified.

RECOMMENDATION: Clinical correlation and routine follow-up per clinical guidelines.`,
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
    clinicalPlan: `The thyroid biopsy shows a benign (non-cancerous) nodule. No signs of thyroid cancer were found.

**Management Plan:**
1. Continue routine monitoring
2. Repeat thyroid ultrasound in 12-18 months
3. Annual clinical examination
4. No medications or surgery needed at this time
5. Monitor for any changes in nodule size or symptoms`,
    patientMessage: `Dear Mr. Chen,

Your thyroid biopsy results are reassuring. The test shows a benign (non-cancerous) nodule in your thyroid. No signs of cancer were found.

What this means:
- The nodule is not cancerous
- No treatment or surgery is needed at this time
- Routine monitoring is recommended

Next steps:
- Follow-up thyroid ultrasound in 12-18 months
- Continue annual check-ups with your doctor
- Let us know if you notice any changes in swelling or have new symptoms

This is a very common finding and does not typically require treatment. We'll keep an eye on it with regular monitoring.

Feel free to contact us if you have any questions.

Best regards,
Your Endocrinology Team`
  },
  {
    id: 'RPT-004',
    patientName: 'Emily Rodriguez',
    patientMRN: 'MRN-98765',
    patientDOB: '1955-05-18',
    diagnosis: 'Pending Analysis',
    category: 'Abnormal',
    receivedDate: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    status: 'analyzing',
    priority: 'stat',
    specimenType: 'Breast core biopsy',
    rawReport: 'Report is being processed by AI agent...',
  }
];
