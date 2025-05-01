document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // add event listener of compose WHEN the document is loaded so it does not stack event listeners
  const form = document.querySelector("#compose-form")
  form.addEventListener('submit', function(event){
    event.preventDefault();
    // get information of email
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    // post information to server
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result); //print result
      load_mailbox('sent');
    });
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Load Email
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails); //check output

    emails.forEach(email => {
      const Newemail = document.createElement('div')
      Newemail.classList.add('email')
      
      Newemail.style.display = "flex";
      Newemail.style.border = '1px solid black';
      Newemail.style.padding = '10px';
      Newemail.style.justifyContent = 'space-between';

      if (email.read == true){
        Newemail.style.backgroundColor = '#b1b1b1';
      } 

      const leftspan = document.createElement('span');
      leftspan.innerHTML = `<strong>${email.sender}</strong> ${email.subject}`;

      const rightspan = document.createElement('span')
      rightspan.innerHTML = `<i>${email.timestamp}`

      Newemail.appendChild(leftspan);
      Newemail.appendChild(rightspan);
      
      Newemail.addEventListener('click', () => load_email(email.id));

      document.querySelector('#emails-view').append(Newemail);
    });
  });
}

function load_email(id) {
  document.querySelector('#emails-view').innerHTML = "";

  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      console.log(email); // See structure

      const details = document.createElement('div');
      details.innerHTML = `
        <h4><strong>From:</strong> ${email.sender}</h4>
        <h4><strong>To:</strong> ${email.recipients.join(', ')}</h4>
        <h4><strong>Subject:</strong> ${email.subject}</h4>
        <h6><strong>Timestamp:</strong> ${email.timestamp}</h6>
        <hr>
        <p>${email.body}</p>
      `;

      if (email.sender != useremail){
        // Create Archive Button
        const archive = document.createElement('button');
        archive.classList.add('btn', 'btn-primary');
        if (email.archived == true){
          archive.textContent = "Unarchive";
          archive.classList.remove('btn', 'btn-primary');
          archive.classList.add('btn', 'btn-sm', 'btn-outline-primary');
          archive.style.height = "40px";
          archive.style.fontSize = "16px";
        }
        else {
          archive.textContent = "Archive";
        }

        // Add Event Listener
        archive.addEventListener("click", ()=> archive_email(email.id, email.archived));
        details.insertBefore(archive, details.children[4]);

        // Create Reply button
        const reply = document.createElement('button');
        reply.classList.add('btn', 'btn-primary');
        reply.textContent = "Reply";
        reply.style.width = '75px';
        reply.style.marginLeft = '20px';

        reply.addEventListener("click", ()=> reply_email(email.id))
        details.insertBefore(reply, details.children[5]);
      }

      document.querySelector('#emails-view').appendChild(details);
    });
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}
function archive_email(id, isarchived){
  if (isarchived == false){
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    .then(() => {
      load_mailbox('inbox')
    });
  }
  else{
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(() => {
      load_mailbox('inbox')
    });
  }
}
function reply_email(id){
 
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#compose-heading').innerHTML = "Reply"

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
  document.querySelector('#compose-recipients').value = email.sender;
  document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}`;
  });
}