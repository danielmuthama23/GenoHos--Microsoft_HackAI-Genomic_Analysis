import React, { useState } from 'react';
import { Form, Button, Alert, Row, Col } from 'react-bootstrap';
import { validatePatientData } from '../utils/validation';

const PatientForm = ({ onAddPatient }) => {
  const [patient, setPatient] = useState({
    name: '',
    email: '',
    age: '',
    weight: '',
    location: '',
    stage: '',
    dateDiagnosed: ''
  });
  
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setPatient(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validatePatientData(patient);
    
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setSuccess(false);
    } else {
      setErrors({});
      onAddPatient(patient);
      setPatient({
        name: '',
        email: '',
        age: '',
        weight: '',
        location: '',
        stage: '',
        dateDiagnosed: ''
      });
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    }
  };

  return (
    <div className="form-container">
      <h2>Patient Information</h2>
      <Form onSubmit={handleSubmit}>
        {success && <Alert variant="success">Patient data recorded successfully!</Alert>}
        
        <Row>
          <Col md={6}>
            <Form.Group controlId="name">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={patient.name}
                onChange={handleChange}
                isInvalid={!!errors.name}
              />
              <Form.Control.Feedback type="invalid">
                {errors.name}
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
          <Col md={6}>
            <Form.Group controlId="email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={patient.email}
                onChange={handleChange}
                isInvalid={!!errors.email}
              />
              <Form.Control.Feedback type="invalid">
                {errors.email}
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
        </Row>

        <Row>
          <Col md={4}>
            <Form.Group controlId="age">
              <Form.Label>Age</Form.Label>
              <Form.Control
                type="number"
                name="age"
                value={patient.age}
                onChange={handleChange}
                isInvalid={!!errors.age}
              />
              <Form.Control.Feedback type="invalid">
                {errors.age}
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group controlId="weight">
              <Form.Label>Weight (kg)</Form.Label>
              <Form.Control
                type="number"
                name="weight"
                value={patient.weight}
                onChange={handleChange}
                isInvalid={!!errors.weight}
              />
              <Form.Control.Feedback type="invalid">
                {errors.weight}
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
          <Col md={4}>
            <Form.Group controlId="stage">
              <Form.Label>Cancer Stage</Form.Label>
              <Form.Control
                as="select"
                name="stage"
                value={patient.stage}
                onChange={handleChange}
                isInvalid={!!errors.stage}
              >
                <option value="">Select stage</option>
                <option value="0">0 - Carcinoma in situ</option>
                <option value="I">I</option>
                <option value="II">II</option>
                <option value="III">III</option>
                <option value="IV">IV</option>
              </Form.Control>
              <Form.Control.Feedback type="invalid">
                {errors.stage}
              </Form.Control.Feedback>
            </Form.Group>
          </Col>
        </Row>

        <Form.Group controlId="location">
          <Form.Label>Location (City/Region)</Form.Label>
          <Form.Control
            type="text"
            name="location"
            value={patient.location}
            onChange={handleChange}
            isInvalid={!!errors.location}
          />
          <Form.Control.Feedback type="invalid">
            {errors.location}
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group controlId="dateDiagnosed">
          <Form.Label>Date Diagnosed</Form.Label>
          <Form.Control
            type="date"
            name="dateDiagnosed"
            value={patient.dateDiagnosed}
            onChange={handleChange}
            isInvalid={!!errors.dateDiagnosed}
          />
          <Form.Control.Feedback type="invalid">
            {errors.dateDiagnosed}
          </Form.Control.Feedback>
        </Form.Group>

        <Button variant="primary" type="submit" className="submit-btn">
          Record Patient Data
        </Button>
      </Form>
    </div>
  );
};

export default PatientForm;