import {useState, useEffect} from 'react'

const ContactForm = ({existingContact = {}, updateCallback}) => {
    const [name, setName] = useState(existingContact.name || '')
    const [email, setEmail] = useState(existingContact.email || '')
    const [phone, setPhone] = useState(existingContact.phone || '')

    const updating = Object.entries(existingContact).length !== 0

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            name,
            email,
            phone
        }

        const url = "http://localhost:8080/api/contacts/" + (updating ? `update/${existingContact.id}` : "create")
        const method = (updating ? "PATCH" : "POST")

        const options = {
            body: JSON.stringify(data),
            method: method,
            headers:{
                "Content-Type": "application/json",
            }
        }

        const response = await fetch(url, options)
        if(response.status !== 200 && response.status !== 201){
            const data = await response.json()
            alert(data.message)
        }else{
            updateCallback()
        }
    }

    return <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="name">Name</label>
            <input type="text" id="name" name="name" value={name} onChange={(e)=>setName(e.target.value)}/>
        </div>
        <div>
            <label htmlFor="email">Email</label>
            <input type="text" id="email" name="email" value={email} onChange={(e)=>setEmail(e.target.value)}/>
        </div>
        <div>
            <label htmlFor="phone">Phone</label>
            <input type="text" id="phone" name="phone" value={phone} onChange={(e) => setPhone(e.target.value)}/>
        </div>
        <button type='submit'>{updating ? "Update Contact" : "Create Contact"}</button>
    </form>
}

export default ContactForm