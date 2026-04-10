// Coming Soon Popup Functionality
function showComingSoonPopup(moduleName) {
  // Create modal if it doesn't exist
  if (!document.getElementById('comingSoonModal')) {
    const modal = document.createElement('div');
    modal.id = 'comingSoonModal';
    modal.className = 'coming-soon-modal';
    modal.innerHTML = `
      <div class='coming-soon-content'>
        <div class='coming-soon-icon'>🚧</div>
        <h2 id='comingSoonTitle'>Module Coming Soon!</h2>
        <p id='comingSoonMessage'>This module is currently under development.</p>
        <div class='coming-soon-features'>
          <h3>What we're working on:</h3>
          <ul>
            <li>✓ Advanced OCR technology</li>
            <li>✓ Image forgery detection</li>
            <li>✓ Document authenticity verification</li>
            <li>✓ Tamper detection algorithms</li>
          </ul>
        </div>
        <button class='coming-soon-close-btn' onclick='closeComingSoonPopup()'>
          <i class='fas fa-times'></i> Close
        </button>
      </div>
    `;
    document.body.appendChild(modal);
    
    // Add click outside to close
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        closeComingSoonPopup();
      }
    });
  }
  
  // Update content
  const title = document.getElementById('comingSoonTitle');
  const message = document.getElementById('comingSoonMessage');
  
  title.textContent = moduleName + ' - Coming Soon!';
  message.textContent = 'The ' + moduleName + ' module is currently under development and will be available soon!';
  
  // Show modal
  const modal = document.getElementById('comingSoonModal');
  modal.classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeComingSoonPopup() {
  const modal = document.getElementById('comingSoonModal');
  if (modal) {
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
  }
}

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeComingSoonPopup();
  }
});
