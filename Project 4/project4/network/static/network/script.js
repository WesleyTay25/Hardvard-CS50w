document.addEventListener("DOMContentLoaded", function(){

    const buttons = document.querySelectorAll(".edit");
    buttons.forEach(button => {
        button.addEventListener("click", function(event){
            event.preventDefault();
            const div = this.closest('div');
            const content = div.querySelector('p');
            console.log(div);
            const divcontents = div.innerHTML; // save its innerHTML
            div.innerHTML = "";
            const postid = div.dataset.postid;

            //create text area
            const textarea = document.createElement('textarea');
            textarea.rows = 4;
            textarea.cols = 50;
            textarea.classList.add("form-control");
            textarea.value = `Edit: ${content.textContent}`;
            textarea.style.marginBottom = "10px";
            

            const save = document.createElement('button');
            save.classList.add("btn", "btn-primary");
            save.style.height = "40px";
            save.style.fontSize = "16px";
            save.style.width = "60px";
            save.textContent = "Save";
            save.addEventListener("click", ()=> edit_function(div, divcontents, postid));

            div.appendChild(textarea);
            div.appendChild(save);
        })
    })
    const likes = document.querySelectorAll('.like');
    likes.forEach(like => {
        like.addEventListener('click', function(event){
            const div = this.closest('div');
            const postid = div.dataset.postid;
            event.preventDefault();
            fetch("/like_post/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
                },
                body: JSON.stringify({
                    "postid": postid
                })    
            })
            .then(response => response.json())
            .then(data => {
                if (data.likecount != undefined) {
                    this.querySelector(".likecount").textContent = data.likecount;
                }
            })
        })
    })
})
function edit_function(div, divcontents, postid){
    console.log('editing', div);
    const updatedtext = div.querySelector('textarea').value;
    console.log(updatedtext);

    fetch(`/edit_post/${postid}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
            "content": updatedtext,
            "edited": true
        })
    })
    .then(response => {
        if(response.ok) {
            div.innerHTML = divcontents;
            div.querySelector("p").textContent = updatedtext;
            if (div.querySelectorAll("i").length < 2) {
            const edited = document.createElement('i');
            edited.textContent = "Edited";
            div.appendChild(edited);
            }
        }
        else {
            alert("Failed to update post.");
        }
    })
}
