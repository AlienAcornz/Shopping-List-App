const BASE_URL = "http://127.0.0.1:8000"

export async function shareList({list}) {
    function removeIds(obj) {
        if (Array.isArray(obj)) {
            return obj.map(removeIds); // recursively repeats this function over any children. This is the base case
        }

        if (obj !== null && typeof obj === "object") {
            const result = {};
            for (const key in obj) {
                if (key !== "id") {
                    result[key] = removeIds(obj[key]); // appends the item to the result as long as it is not an object
                }
            }
            return result; // returns the result
        }

        return obj; // returns the object of the overall structure. This is the inital {} set.
    }

    const payload = removeIds(list)

    const response = await fetch((`${BASE_URL}/create`), {
        method: "POST",
        body: JSON.stringify(payload)
    })

    return await response.json()
}