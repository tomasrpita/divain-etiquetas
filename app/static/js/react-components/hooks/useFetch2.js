
export const useFetch2 = (initialUrl='', initialMethod = 'GET', initialBody = null) => {
    const [url, setUrl] = React.useState(initialUrl);
    const [method, setMethod] = React.useState(initialMethod);
    const [body, setBody] = React.useState(initialBody);
    const [state, setState] = React.useState({
        data: null,
        isLoading: false,
        hasError: null
    });

    // console.log({url, method, body});
    // console.log({state});

    React.useEffect(() => {
        const fetchData = async () => {
            if (!url) return;
            setState({ ...state, isLoading: true });

            try {
                const options = {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                };

                if (body && method !== 'GET') {
                    options.body = JSON.stringify(body);
                }

                const response = await fetch(url, options);
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error.message);
                }

                const data = await response.json();
                setState({ data, isLoading: false, error: null });
            } catch (error) {
                setState({ data: null, isLoading: false, hasError: error.message });
            }
        };

        fetchData();
    }, [url, method, body]);

    return [state, setUrl, setMethod, setBody];
};
