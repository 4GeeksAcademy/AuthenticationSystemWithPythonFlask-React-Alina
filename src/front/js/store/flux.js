const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			users: [],
			people: [],
			peopleDetails: {},
			planets: [],
			planetsDetails: {},
			vehicles: [],
			vehiclesDetails: {},
			favorites: []
		},
		
		actions: {
			getEntities : async(type) => {
				const res = await fetch(`https://www.swapi.tech/api/${type}`)
				const data = await res.json()
				setStore({[`${type}`]: data.results})
			},

			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			
			login: async(email, password) => {
				try{
					let response = await fetch (`${process.env.BACKEND_URL}api/login`, {
						method: "POST",
						headers: {
							"Content-Type" : "application/json"
						},
						body: JSON.stringify({
							"email" : email,
							"password" : password
						})
					})

					const data = await response.json()
					console.log(data.msg)
					if (!data.msg){
						localStorage.setItem("token", data.access_token);
					}
					return true

				} catch(error) {
					return false
				}
			},

			signIn: async(email, password, name) => {
				try{
					let response = await fetch (`https://crispy-guide-x7qjg4qxw5qfp65p-3001.app.github.dev/api/register`, {
						method: "POST",
						headers: {
							"Content-Type" : "application/json"
						},
						body: JSON.stringify({
							"email" : email,
							"password" : password,
							"name": name,
							"is_active" : true
						})
					})

					const data = await response.json()
					if (!data.msg){
						localStorage.setItem("token", data.access_token)
					}
					return true

				} catch(error) {
					return false
				}
			},

			logOut: async() => {
				console.log("ASDA")
				localStorage.removeItem("token");
			},
			
			getEntitiesDetails: async(id, type) => {
				const result = await fetch(`https://www.swapi.tech/api/${type}/${id}`)
				const data = await result.json()
				setStore({[`${type}Details`]: data.result.properties})
			},

			saveFavorite: (id, name, type) => {
				setStore({favorites:[...getStore().favorites,{name: name, id: id, type: type}]})
			},
			
			removeFavorite: (name) => {
				const filteredArray  = getStore().favorites.filter((item) => item.name != name);
				setStore({favorites: filteredArray})
			}
		}
		
	};
};

export default getState;

