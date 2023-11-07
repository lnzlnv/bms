import { ref } from 'vue';

const page = (apiCall, defLimit=10) => {
	const pageNumber = ref(0)
	const limit = defLimit

	const next = (url) => {
		pageNumber.value += 1;
		const pagination = url + `?limit=${limit}&offset=${limit*pageNumber.value}`
		apiCall(pagination)
	}

	const previous = (url) => {
		pageNumber.value -= 1
		const pagination = url + `?limit=${limit}&offset=${limit*pageNumber.value}`
		apiCall(pagination)
	}

	return {
		pageNumber,
		limit,
		next,
		previous
	}
}

export { page }