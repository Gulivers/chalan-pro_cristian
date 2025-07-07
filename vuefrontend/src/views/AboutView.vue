<template>
  <section class="py-5 bg-light">
    <div class="container">
      <!-- Title Section -->
      <div class="row justify-content-center">
        <div class="col-lg-8 text-center">
          <h3 class="display-5 text-primary">About Chalan-Pro</h3>
          <p class="lead mb-5">An advanced solution for contract and work pricing management in construction projects.</p>
        </div>
      </div>

      <!-- Content Section -->
      <div class="row">
        <div class="col-lg-10 mx-auto text-justify">
          <!-- What is Chalan-Pro? -->
          <h3 class="text-primary mb-4">What is Chalan-Pro?</h3>
          <p class="text-muted mb-4">
            <strong>Chalan-Pro</strong> is a web-based application designed to efficiently manage contracts, communities, and work crews in construction projects. It provides users with a unified platform to control everything from contract creation to work price management. Its primary focus is on automating and simplifying complex workflows, reducing the need for manual processes, and increasing productivity.
          </p>

          <!-- What is Chalan-Pro for? -->
          <h3 class="text-primary mb-4">What is Chalan-Pro for?</h3>
          <p class="text-muted mb-4">
            <strong>Chalan-Pro</strong> is designed to reduce costs in project management by optimizing resource use and eliminating inefficiencies. It centralizes all information on one platform, helping companies avoid costly errors, improve pricing accuracy, and minimize downtime for work crews. 
          </p>
          <p class="text-muted mb-4">
            By enhancing transparency and traceability in project management, Chalan-Pro allows for detailed tracking of contracts and work prices. Its web-based platform offers real-time access from anywhere, enabling teams and managers to coordinate effectively and make informed decisions with up-to-date data. This not only improves overall project efficiency but also results in significant cost savings by reducing errors, minimizing downtime, and optimizing resource use.
          </p>

          <!-- Advantages of Chalan-Pro -->
          <h3 class="text-primary mb-4">Advantages of Being a WebApp</h3>
          <ul class="list-group list-group-flush mb-4 text-muted">
            <li class="list-group-item"><strong>Accessibility:</strong> As a web application, Chalan-Pro is available from any device with internet access, allowing users to manage their projects anytime, anywhere.</li>
            <li class="list-group-item"><strong>Scalability:</strong> Built on Django and Vue.js, the platform is scalable, adapting to the changing needs of projects without compromising performance.</li>
            <li class="list-group-item"><strong>Security:</strong> Django, known for its security features, integrates protection against common vulnerabilities, such as SQL injection and CSRF attacks, ensuring confidential data remains secure.</li>
            <li class="list-group-item"><strong>Modularity and Customization:</strong> With a clear separation between frontend and backend, Chalan-Pro is customizable for each company's specific needs, without affecting the core functionality.</li>
          </ul>

          <!-- A Future Powered by AI -->
          <h3 class="text-primary mb-4">A Future Powered by Artificial Intelligence</h3>
          <p class="text-muted mb-4">
            One of the future visions for <strong>Chalan-Pro</strong> is to integrate advanced artificial intelligence (AI) technologies to revolutionize blueprint analysis and project management. Since it is built in Python, a language widely used in AI, Chalan-Pro is well-positioned to automate processes such as automatic blueprint analysis.
          </p>
          <p class="text-muted mb-4">
            Imagine a future where users upload a blueprint, and the system automatically identifies work areas, estimates costs, generates contracts, and proposes improvements based on historical data. This advancement will not only save time and resources but also ensure greater accuracy, pushing monetary savings to even higher levels.
          </p>
          <p class="text-muted mb-4">
            With <strong>Chalan-Pro</strong>, users are on the path to more efficient, precise, and economically optimized construction project management.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// No additional script is required for this section
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap');

section {
  font-family: 'Montserrat', sans-serif;
}

h2, h3 {
  font-weight: 500;
  color: #395ecb;
}

p, ul, li {
  font-weight: 500;
  color: #474f57;
  font-size: 16px;
}

.lead {
  font-weight: 500;
  font-size: 16px;
}

.list-group-item {
  border: 0;
  background: transparent;
  font-size: 16px;
}

.container {
  max-width: 1140px;
}

.text-muted {
  color: #4a4a4a !important; /* Cambia el gris predeterminado */
  font-size: 16px; /* Mantiene la legibilidad */
}

@media (max-width: 768px) {
  h2 {
    font-size: 2.5rem;
  }
  h3 {
    font-size: 1.75rem;
  }
}
</style>
