import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form,
  Pagination,
  Spinner,
  Alert
} from 'react-bootstrap';
import { generateCSV } from '../utils/csvGenerator';
import { patientService } from '../services/patient.service';

const DataTable = ({ authToken }) => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [patientsPerPage] = useState(5);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [currentPatient, setCurrentPatient] = useState(null);

  // Load patients from backend
  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await patientService.getPatients();
        setPatients(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load patient records');
        setLoading(false);
        console.error('Error loading patients:', err);
      }
    };
    
    fetchPatients();
  }, []);

  // Pagination logic
  const indexOfLastPatient = currentPage * patientsPerPage;
  const indexOfFirstPatient = indexOfLastPatient - patientsPerPage;
  const currentPatients = patients.slice(indexOfFirstPatient, indexOfLastPatient);
  const totalPages = Math.ceil(patients.length / patientsPerPage);

  const handleEdit = (patient) => {
    setCurrentPatient(patient);
    setShowEditModal(true);
  };

  const handleSave = async () => {
    try {
      await patientService.updatePatient(currentPatient._id, currentPatient, authToken);
      const updatedPatients = patients.map(p => 
        p._id === currentPatient._id ? currentPatient : p
      );
      setPatients(updatedPatients);
      setShowEditModal(false);
    } catch (err) {
      setError('Failed to update patient record');
      console.error('Error updating patient:', err);
    }
  };

  const handleDelete = (patient) => {
    setCurrentPatient(patient);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    try {
      await patientService.deletePatient(currentPatient._id, authToken);
      const updatedPatients = patients.filter(p => p._id !== currentPatient._id);
      setPatients(updatedPatients);
      setShowDeleteModal(false);
    } catch (err) {
      setError('Failed to delete patient record');
      console.error('Error deleting patient:', err);
    }
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

  if (loading) {
    return (
      <div className="text-center mt-5">
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p>Loading patient records...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="danger" className="mt-3">
        {error}
      </Alert>
    );
  }

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
              {currentPatients.map((patient) => (
                <tr key={patient._id}>
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
                  <td>{new Date(patient.createdAt).toLocaleDateString()}</td>
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
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              value={currentPatient?.email || ''}
              onChange={(e) => setCurrentPatient({...currentPatient, email: e.target.value})}
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
          Are you sure you want to delete {currentPatient?.name}'s record? This action cannot be undone.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            Delete Permanently
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

const getStageColor = (stage) => {
  switch(stage) {
    case 'Stage 0': return 'info';
    case 'Stage I': return 'primary';
    case 'Stage II': return 'warning';
    case 'Stage III': return 'danger';
    case 'Stage IV': return 'dark';
    default: return 'secondary';
  }
};

export default DataTable;