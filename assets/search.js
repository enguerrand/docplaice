const e = React.createElement;

const EVENT_TYPES = ["change", "paste", "keyup", "focus"];
const MAX_RESULT_COUNT = 20;

class SearchResults extends React.Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.handleFocusLoss = this.handleFocusLoss.bind(this);
        this.state = {};
        this.monitorFocus = true;
        for (const key in search_index) {
            this.state[key] = false
        }
    }

    handleChange() {
        const search_string = document.getElementById("search").value;
        this.setState((prevState, prevProps) => {
            let nextState = {};
            for (const key in search_index) {
                if (search_string !== "" && key.includes(search_string) && !prevState[key]) {
                    nextState[key] = true;
                } else if (search_string === "" || !key.includes(search_string) && prevState[key]) {
                    nextState[key] = false;
                }
            }
            return nextState;
        });
        console.log(search_string);
    }

    handleFocusLoss(){
        if (this.monitorFocus) {
            this.setState((prevState, prevProps) => {
                let nextState = {};
                for (const key in search_index) {
                    if (prevState[key]) {
                        nextState[key] = false;
                    }
                }
                return nextState;
            });
        }
    }

    componentDidMount() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.addEventListener(t, this.handleChange);
        }
        element.addEventListener("blur", this.handleFocusLoss);
    }

    componentWillUnmount() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.removeEventListener(t, this.handleChange);
        }
        element.removeEventListener("blur", this.handleFocusLoss);
    }

    render() {
        let entries = [];
        keysLoop:
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
                                    onMouseDown: () => {this.monitorFocus = false},
                                    href: match["url"]
                                },
                                match["name"]
                            )
                        );
                        if (entries.length >= MAX_RESULT_COUNT) {
                            break keysLoop;
                        }
                    }
                }
            }
        let searchResultsClass;
        if (entries.length > 0) {
            searchResultsClass = "search-results-content";
        } else {
            searchResultsClass = "search-results-empty";
        }
        return e(
            'div',
            {
                className: searchResultsClass
            },
            entries
        )
    }
}

window.onload = function () {
    const domContainer = document.querySelector('#search-results');
    ReactDOM.render(e(SearchResults), domContainer);
}