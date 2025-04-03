import React, { useState } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form,   // <-- This was missing
  Pagination 
} from 'react-bootstrap';
import { generateCSV } from '../utils/csvGenerator';

const DataTable = ({ patients, onDeletePatient, onUpdatePatient }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [patientsPerPage] = useState(5);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [currentPatient, setCurrentPatient] = useState(null);

  // Pagination logic
  const indexOfLastPatient = currentPage * patientsPerPage;
  const indexOfFirstPatient = indexOfLastPatient - patientsPerPage;
  const currentPatients = patients.slice(indexOfFirstPatient, indexOfLastPatient);
  const totalPages = Math.ceil(patients.length / patientsPerPage);

  const handleEdit = (patient) => {
    setCurrentPatient(patient);
    setShowEditModal(true);
  };

  const handleSave = () => {
    onUpdatePatient(currentPatient);
    setShowEditModal(false);
  };

  const handleDelete = (patient) => {
    setCurrentPatient(patient);
    setShowDeleteModal(true);
  };

  const confirmDelete = () => {
    onDeletePatient(currentPatient);
    setShowDeleteModal(false);
  };

  const downloadCSV = () => {
    const csvContent = generateCSV(patients);
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'breast_cancer_patients.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="table-container">
      <h2>Recorded Patients</h2>
      {patients.length > 0 ? (
        <>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Age</th>
                <th>Weight</th>
                <th>Location</th>
                <th>Stage</th>
                <th>Diagnosed</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentPatients.map((patient, index) => (
                <tr key={index}>
                  <td>{patient.name}</td>
                  <td>{patient.email}</td>
                  <td>{patient.age}</td>
                  <td>{patient.weight} kg</td>
                  <td>{patient.location}</td>
                  <td>
                    <span className={`badge bg-${getStageColor(patient.stage)}`}>
                      {patient.stage}
                    </span>
                  </td>
                  <td>{patient.dateDiagnosed}</td>
                  <td>
                    <Button variant="outline-primary" size="sm" onClick={() => handleEdit(patient)}>
                      Edit
                    </Button>{' '}
                    <Button variant="outline-danger" size="sm" onClick={() => handleDelete(patient)}>
                      Delete
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>

          {totalPages > 1 && (
            <Pagination className="justify-content-center mt-3">
              <Pagination.Prev 
                onClick={() => setCurrentPage(p => Math.max(p - 1, 1))} 
                disabled={currentPage === 1}
              />
              {Array.from({ length: totalPages }, (_, i) => (
                <Pagination.Item
                  key={i + 1}
                  active={i + 1 === currentPage}
                  onClick={() => setCurrentPage(i + 1)}
                >
                  {i + 1}
                </Pagination.Item>
              ))}
              <Pagination.Next 
                onClick={() => setCurrentPage(p => Math.min(p + 1, totalPages))} 
                disabled={currentPage === totalPages}
              />
            </Pagination>
          )}

          <Button variant="success" onClick={downloadCSV} className="mt-3">
            Download CSV
          </Button>
        </>
      ) : (
        <p>No patient data recorded yet.</p>
      )}

      {/* Edit Modal */}
      <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Patient</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group className="mb-3">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              value={currentPatient?.name || ''}
              onChange={(e) => setCurrentPatient({...currentPatient, name: e.target.value})}
            />
          </Form.Group>
          {/* Add other fields similarly */}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowEditModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Delete Modal */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete {currentPatient?.name}'s record?
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            Delete
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

const getStageColor = (stage) => {
  switch(stage) {
    case '0': return 'info';
    case 'I': return 'primary';
    case 'II': return 'warning';
    case 'III': return 'danger';
    case 'IV': return 'dark';
    default: return 'secondary';
  }
};

export default DataTable;