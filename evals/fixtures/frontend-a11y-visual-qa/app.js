const statusCards = document.querySelector('#status-cards');
const form = document.querySelector('#settings-form');
const formMessage = document.querySelector('#form-message');
const openInvite = document.querySelector('#open-invite');
const drawer = document.querySelector('#invite-drawer');
const closeInvite = document.querySelector('#close-invite');
const cancelInvite = document.querySelector('#cancel-invite');
const inviteEmail = document.querySelector('#invite-email');
const inviteRole = document.querySelector('#invite-role');
const sendInvite = document.querySelector('#send-invite');
const inviteMessage = document.querySelector('#invite-message');
const startBatch = document.querySelector('#start-batch');
const batchMessage = document.querySelector('#batch-message');
const toast = document.querySelector('#toast');

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  window.setTimeout(() => toast.classList.remove('show'), 2200);
}

function openDrawer() {
  drawer.hidden = false;
  document.body.style.overflow = 'hidden';
  inviteEmail.focus();
}

function closeDrawer() {
  drawer.hidden = true;
  document.body.style.overflow = '';
  inviteMessage.textContent = '';
  inviteEmail.value = '';
  inviteRole.value = 'Manager';
  openInvite.focus();
}

window.setTimeout(() => {
  const card = document.createElement('article');
  card.className = 'status-card late';
  card.innerHTML = '<span class="status-label">Sensor</span><strong>Synced</strong><span class="status-foot">Added after initial render</span>';
  statusCards.appendChild(card);
}, 1100);

form.addEventListener('submit', (event) => {
  event.preventDefault();
  formMessage.textContent = 'Settings saved';
  showToast('Settings saved');
});

startBatch.addEventListener('click', () => {
  batchMessage.textContent = 'Next batch started';
  showToast('Batch started');
});

openInvite.addEventListener('click', openDrawer);
cancelInvite.addEventListener('click', closeDrawer);
closeInvite.addEventListener('click', closeDrawer);

drawer.addEventListener('click', (event) => {
  if (event.target === drawer) {
    closeDrawer();
  }
});

sendInvite.addEventListener('click', () => {
  inviteMessage.textContent = 'Invite sent';
  showToast('Invite sent');
});
