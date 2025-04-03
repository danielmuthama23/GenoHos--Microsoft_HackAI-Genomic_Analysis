export const validatePatientData = (patient) => {
  const errors = {};
  
  if (!patient.name.trim()) {
    errors.name = 'Name is required';
  } else if (patient.name.length < 2) {
    errors.name = 'Name must be at least 2 characters';
  }
  
  if (!patient.email) {
    errors.email = 'Email is required';
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(patient.email)) {
    errors.email = 'Email is invalid';
  }
  
  if (!patient.age) {
    errors.age = 'Age is required';
  } else if (patient.age < 18 || patient.age > 120) {
    errors.age = 'Age must be between 18 and 120';
  }
  
  if (!patient.weight) {
    errors.weight = 'Weight is required';
  } else if (patient.weight < 30 || patient.weight > 300) {
    errors.weight = 'Weight must be between 30 and 300 kg';
  }
  
  if (!patient.location.trim()) {
    errors.location = 'Location is required';
  }
  
  if (!patient.stage) {
    errors.stage = 'Cancer stage is required';
  }
  
  if (!patient.dateDiagnosed) {
    errors.dateDiagnosed = 'Diagnosis date is required';
  } else if (new Date(patient.dateDiagnosed) > new Date()) {
    errors.dateDiagnosed = 'Date cannot be in the future';
  }
  
  return errors;
};