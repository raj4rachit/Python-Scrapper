import {useEffect, useState} from 'react'
import ContactList from "./ContactList.jsx";
import './App.css'
import ContactForm from "../public/ContactForm.jsx";

function App() {
    const [contacts, setContacts] = useState([])
    const[isModalOpen, setIsModalOpen] = useState(false)
    const [currentContact, setCurrentcontact] = useState({})

    useEffect(() => {
        fetchContacts()
    }, []);
    const fetchContacts = async () => {
        const response = await fetch('http://localhost:8080/api/contacts', {})
        const data = await response.json()
        setContacts(data.contacts)
    }

    const closeModal = () => {
        setIsModalOpen(false)
        setCurrentcontact({})
    }

    const openCreateModal = ()=>{
        if(!isModalOpen) setIsModalOpen(true)
    }

    const openEditModal=(contact) =>{
        if(isModalOpen) return
        setCurrentcontact(contact)
        setIsModalOpen(true)
    }

    const onUpdate = () => {
        closeModal()
        fetchContacts()
    }

  return <>
      <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate}/>
      <button onClick={openCreateModal}>Create a New Contact</button>
      {
          isModalOpen && <div className="modal">
              <div className="modal-content">
                  <span>Add Contact</span>
                  <span className="close" onClick={closeModal}>&times;</span>
                  <hr/>
                  <ContactForm existingContact={currentContact} updateCallback={onUpdate}/>
              </div>
          </div>
      }
  </>
}

export default App
