// Auto-show any Bootstrap toasts (flash messages)
document.querySelectorAll('.toast').forEach(t => {
  const toast = new bootstrap.Toast(t, { delay: 3500 });
  toast.show();
});

// Delete confirmation modal
let pendingDeleteForm = null;

document.querySelectorAll('.delete-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    pendingDeleteForm = e.currentTarget.closest('form');
    const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    modal.show();
  });
});

const confirmBtn = document.getElementById('confirmDeleteBtn');
if (confirmBtn) {
  confirmBtn.addEventListener('click', () => {
    if (pendingDeleteForm) pendingDeleteForm.submit();
  });
}
