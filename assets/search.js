const e = React.createElement;

const EVENT_TYPES = ["change", "paste", "keyup", "focus"];
const MAX_RESULT_COUNT = 20;

class SearchResults extends React.Component {
    constructor(props) {
        super(props);
        this.handleArrowKey = this.handleArrowKey.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleEvent = this.handleEvent.bind(this);
        this.handleFocusLoss = this.handleFocusLoss.bind(this);
        this.state = {
            matches: [],
            selectedIndex: -1
        };
        this.monitorFocus = true;
    }

    handleArrowKey(event) {
        const element = document.getElementById("search");
        console.log(event.key);
        switch(event.key) {
            case "ArrowUp": {
                element.select();
                return false;
            }
            case "ArrowDown": {
                element.select();
                return false;
            }
            default:
                return true;
        }
    }

    handleInputChange() {
        const search_string = document.getElementById("search").value;
        let nextMatches = [];
        for (const key in search_index) {
            let search_matches = key.toLowerCase().includes(search_string.toLowerCase());
            if (search_string !== "" && search_matches) {
                nextMatches.push(key);
            }
        }
        this.setState({
            matches: nextMatches
        });
        return true;
    }

    handleEvent(event) {
        if (event.key !== undefined && event.key.startsWith("Arrow")) {
            return this.handleArrowKey(event);
        } else {
            return this.handleInputChange();
        }
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
            element.addEventListener(t, this.handleEvent);
        }
        element.addEventListener("blur", this.handleFocusLoss);
    }

    componentWillUnmount() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.removeEventListener(t, this.handleEvent);
        }
        element.removeEventListener("blur", this.handleFocusLoss);
    }

    render() {
        let entries = [];
        keysLoop:
            for (const key of this.state.matches) {
                if (this.state.matches.includes(key)) {
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