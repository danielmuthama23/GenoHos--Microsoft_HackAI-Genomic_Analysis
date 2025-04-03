import React, { useState } from 'react';
import PatientForm from './components/PatientForm';
import DataTable from './components/DataTable';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles.css';

function App() {
  const [patients, setPatients] = useState([]);
  const [showTable, setShowTable] = useState(false);

  const addPatient = (patient) => {
    setPatients([...patients, patient]);
    setShowTable(true);
  };

  const deletePatient = (patientToDelete) => {
    setPatients(patients.filter(p => p.email !== patientToDelete.email));
  };

  const updatePatient = (updatedPatient) => {
    setPatients(patients.map(p => 
      p.email === updatedPatient.email ? updatedPatient : p
    ));
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Breast Cancer Patient Recorder</h1>
        <p className="lead">Record and manage patient data efficiently</p>
      </header>
      
      <div className="container-fluid">
        <div className="row">
          <div className="col-lg-6">
            <PatientForm onAddPatient={addPatient} />
          </div>
          <div className="col-lg-6">
            {showTable && (
              <DataTable 
                patients={patients} 
                onDeletePatient={deletePatient}
                onUpdatePatient={updatePatient}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;