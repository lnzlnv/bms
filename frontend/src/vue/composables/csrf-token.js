import axios from "axios";

const setCsrfToken = () => {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  axios.defaults.headers.common['X-CSRFToken'] = csrfToken;
}

export default setCsrfToken