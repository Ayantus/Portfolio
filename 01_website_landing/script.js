document.getElementById('contact-form').addEventListener('submit', function(e){
  e.preventDefault();
  const form = e.target;
  const data = Object.fromEntries(new FormData(form).entries());
  // Demo only: echo the message locally
  document.getElementById('form-status').textContent =
    `Thanks, ${data.name}! I’ll reply to ${data.email} within 24 hours.`;
  form.reset();
});