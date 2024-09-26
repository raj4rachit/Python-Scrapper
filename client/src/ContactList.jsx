import React from 'react';

const ContactList = ({contacts, updateContact, updateCallback}) => {
    const onDelete = async (id) => {
        try {
            const options = {
                method: 'DELETE',
            }
            const response = await fetch(`http://localhost:8080/api/contacts/delete/${id}`,options)
            if (response.status === 200) {
                updateCallback(response)
            }else{
                console.error("Error occured")
            }
        }
        catch (error) {
            console.log(error)
            alert(error)
        }
    }

    return <div>
        <h2>Contacts</h2>
        <table border="1" id="contactList" style={{width: "100%"}}>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
            {contacts.map(contact => (
                <tr key={contact.id}>
                    <td>{contact.name}</td>
                    <td>{contact.email}</td>
                    <td>{contact.phone}</td>
                    <td>
                        <button onClick={()=>updateContact(contact)}>Update</button>
                        <button onClick={()=>onDelete(contact.id)}>Delete</button>
                    </td>
                </tr>
            ))}
            </tbody>
        </table>
    </div>;
}

export default ContactList;