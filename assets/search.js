const e = React.createElement;

const EVENT_TYPES = ["change", "paste", "keyup"];

class SearchResults extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.state = {};
        for (const key in search_index) {
            this.state[key] = false
        }
    }

    handleChange() {
        const search_string = document.getElementById("search").value;
        this.setState((prevState, prevProps) => {
            let nextState = {};
            for (const key in search_index) {
                if (key.includes(search_string) && !prevState[key]) {
                    nextState[key] = true;
                } else if (!key.includes(search_string) && prevState[key]) {
                    nextState[key] = false;
                }
            }
            return nextState;
        });
        console.log(search_string);
    }

    componentDidMount() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.addEventListener(t, this.handleChange);
        }
    }

    componentWillUnmount() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.removeEventListener(t, this.handleChange);
        }
    }

    render() {
        let entries = [];
        for (const key in this.state) {
            if (this.state[key]) {
                const matches = search_index[key];
                for (const resultIndex in matches) {
                    const match = matches[resultIndex];
                    entries.push(
                        e(
                            "a",
                            {
                                key: key + "." + resultIndex,
                                href: match["url"]
                            },
                            match["name"]
                        )
                    );
                }
            }
        }
        return e(
            'div',
            null,
            entries
        )
    }
}

window.onload = function () {
    const domContainer = document.querySelector('#search-results');
    ReactDOM.render(e(SearchResults), domContainer);
}