function likeImage(imageId) {
    fetch(`/like_image/${imageId}`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                alert("Image liked!");
                location.reload(); // Refresh to see the updated like count
            } else {
                alert("You have already liked this image.");
            }
        })
        .catch(error => console.error("Fetch error:", error));
}

function openCommentModal(imageId) {
    fetch(`/get_comments/${imageId}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('commentSection').innerHTML = data;
            document.getElementById('commentForm').onsubmit = function(event) {
                submitComment(event, imageId);
            };
            new bootstrap.Modal(document.getElementById('commentModal')).show();
        });
}

function submitComment(event, imageId) {
    event.preventDefault();
    const commentText = document.querySelector("#commentForm textarea").value;
    fetch(`/comment_image/${imageId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment_text: commentText })
    })
    .then(response => {
        if (response.ok) {
            document.querySelector("#commentForm textarea").value = '';
            openCommentModal(imageId);  // Refresh comments
        } else {
            alert("Error submitting comment.");
        }
    })
    .catch(error => console.error("Fetch error:", error));
}

function deleteImage(imageId) {
    if (confirm("Are you sure you want to delete this image?")) {
        fetch(`/delete_image/${imageId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    alert("Image deleted!");
                    location.reload();  // Refresh the page to update the image list
                } else {
                    alert("Error deleting image.");
                }
            })
            .catch(error => console.error("Fetch error:", error));
    }
}

function openFullScreenModal(imageUrl, imageName) {
    const modal = new bootstrap.Modal(document.getElementById('fullScreenModal'));
    document.getElementById('fullScreenImage').src = imageUrl;
    document.getElementById('fullScreenModalTitle').textContent = imageName;
    modal.show();
}


function editComment(commentId) {
    const newText = prompt("Edit your comment:");
    if (newText) {
        fetch(`/edit_comment/${commentId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ new_text: newText })
        }).then(response => {
            if (response.ok) {
                alert("Comment edited!");
                location.reload();
            } else {
                alert("Error editing comment.");
            }
        });
    }
}

function deleteImage(imageId) {
    if (confirm("Are you sure you want to delete this image?")) {
        fetch(`/delete_image/${imageId}`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    alert("Image deleted!");
                    location.reload();  // Refresh the page to update the image list
                } else {
                    alert("Error deleting image.");
                }
            })
            .catch(error => console.error("Fetch error:", error));
    }
}
