export const generateCSV = (patients) => {
  const headers = [
    'Name', 'Email', 'Age', 'Weight (kg)', 
    'Location', 'Cancer Stage', 'Date Diagnosed'
  ];
  
  const rows = patients.map(patient => [
    patient.name,
    patient.email,
    patient.age,
    patient.weight,
    patient.location,
    patient.stage,
    patient.dateDiagnosed
  ]);
  
  const csvRows = [
    headers.join(','),
    ...rows.map(row => 
      row.map(item => `"${String(item).replace(/"/g, '""')}"`).join(',')
    )
  ];
  
  return csvRows.join('\n');
};