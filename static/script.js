// The generic detection button functionality has been removed as each module has its own specific button
// This section is intentionally left blank for future use if needed

// Scroll to About section
function knowMore() {
  const aboutSection = document.getElementById('about');
  if (aboutSection) {
    aboutSection.scrollIntoView({ behavior: 'smooth' });
  }
}

// Check if user is logged in before redirecting to detection modules
function checkLoginAndRedirect(url) {
  // Make an AJAX call to check if user is logged in
  fetch('/api/status')
    .then(response => response.json())
    .then(data => {
      if (data.logged_in) {
        // User is logged in, go directly to the module
        window.location.href = url;
      } else {
        // User is not logged in, redirect to login with next parameter
        window.location.href = '/login?next=' + encodeURIComponent(url);
      }
    })
    .catch(error => {
      // If there's an error, default to login redirect
      console.error('Error checking login status:', error);
      window.location.href = '/login?next=' + encodeURIComponent(url);
    });
}

// Update fraud stats view when clicking tabs
function updateFraudStats(period) {
  try {
    // fraudData is defined in the page template near the map
    if (typeof fraudData === 'undefined') return;
    const data = fraudData[period] || fraudData['24h'];
    const container = document.getElementById('fraud-stats');
    if (!container) return;

    // Update active tab styling
    document.querySelectorAll('.distribution-tabs .tab').forEach(btn => {
      btn.classList.remove('active');
      if (btn.textContent.trim() === period) {
        btn.classList.add('active');
      }
    });

    // Build HTML for bars
    const entries = [
      ['UPI Fraud','pink'],
      ['Credit Card','orange'],
      ['Identity Theft','purple'],
      ['Phishing','blue'],
      ['Other','gray']
    ];
    container.innerHTML = '';
    entries.forEach(([label, cls]) => {
      const item = data[label] || { cases: 0, percent: 0 };
      const div = document.createElement('div');
      const bar = document.createElement('span');
      bar.className = `bar ${cls}`;
      bar.style.width = (item.percent || 0) + '%';
      bar.setAttribute('aria-hidden','true');
      div.appendChild(bar);
      const text = document.createTextNode(label);
      div.appendChild(text);
      const val = document.createElement('span');
      val.className = 'value';
      val.textContent = `${item.cases || 0} cases ${item.percent || 0}%`;
      div.appendChild(val);
      container.appendChild(div);
    });
  } catch (e) {
    console.error('updateFraudStats error', e);
  }
}

// Initialize default stats view after DOM ready
document.addEventListener('DOMContentLoaded', function() {
  updateFraudStats('24h');
  
  // Add event listeners for all detect buttons
  const detectButtons = document.querySelectorAll('.detect-btn');
  detectButtons.forEach(button => {
    button.addEventListener('click', function() {
      // The buttons already have onclick handlers in the HTML
      // This is just a placeholder in case we need additional functionality
      console.log('Detect button clicked');
    });
  });
});

