const e = React.createElement;

const EVENT_TYPES = ["paste", "keyup", "focus"];
const MAX_RESULT_COUNT = 20;

class SearchResults extends React.Component {
    constructor(props) {
        super(props);
        this.handleArrowKey = this.handleArrowKey.bind(this);
        this.getMatchCount = this.getMatchCount.bind(this);
        this.redirectToSelectedHref = this.redirectToSelectedHref.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleEvent = this.handleEvent.bind(this);
        this.handleFocusLoss = this.handleFocusLoss.bind(this);
        this.removeEventListeners = this.removeEventListeners.bind(this);
        this.state = {
            matches: [],
            selectedIndex: -1
        };
        this.monitorFocus = true;
    }

    handleArrowKey(event) {
        const element = document.getElementById("search");
        switch(event.key) {
            case "ArrowUp": {
                this.setState((state, props) => {
                    const prevIndex = state.selectedIndex;
                    const matchCount = this.getMatchCount(state.matches);
                    let nextIndex = Math.max(-1, prevIndex - 1);
                    if (matchCount === 0) {
                        nextIndex = -1;
                    }
                    return {
                        selectedIndex: nextIndex
                    }
                });
                break;
            }
            case "ArrowDown": {
                this.setState((state, props) => {
                    const prevIndex = state.selectedIndex;
                    const matchCount = this.getMatchCount(state.matches);
                    let nextIndex = Math.min(
                        Math.min(matchCount, MAX_RESULT_COUNT) - 1,
                        prevIndex + 1
                    );
                    if (matchCount === 0) {
                        nextIndex = -1;
                    }
                    return {
                        selectedIndex: nextIndex
                    }
                });
                break;
            }
            case "Enter": {
                // this.removeEventListeners();
                this.redirectToSelectedHref();
                break;
            }
            default:
                return true;
        }
    }

    getMatchCount(matches) {
        let matchCount = 0;
        for (const m of matches) {
            matchCount += search_index[m].length;
        }
        return matchCount;
    }

    redirectToSelectedHref() {
        const selection = document.querySelector("#search-results a.selected");
        if (selection !== null) {
            const href = selection.href;
            if (href !== null && window.location.href !== href) {
                window.location.href = href;
            }
        }

    }

    handleInputChange(event) {
        const search_string = document.getElementById("search").value;
        let nextMatches = [];
        for (const key in search_index) {
            let search_matches = key.toLowerCase().includes(search_string.toLowerCase());
            if (search_string !== "" && search_matches) {
                nextMatches.push(key);
            }
        }
        this.setState({
            matches: nextMatches,
            selectedIndex: -1
        });
        return true;
    }

    handleEvent(event) {
        if (event.key !== undefined && (event.key.startsWith("Arrow") || event.key === "Enter" )) {
            return this.handleArrowKey(event);
        } else {
            return this.handleInputChange(event);
        }
    }

    handleFocusLoss(){
        if (this.monitorFocus) {
            this.setState({
                matches: []
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

    removeEventListeners() {
        const element = document.getElementById("search");
        for (const t of EVENT_TYPES) {
            element.removeEventListener(t, this.handleEvent);
        }
        element.removeEventListener("blur", this.handleFocusLoss);
    }

    componentWillUnmount() {
        this.removeEventListeners();
    }

    render() {
        let entries = [];
        let index = -1;
        keysLoop:
            for (const key of this.state.matches) {
                if (this.state.matches.includes(key)) {
                    const matches = search_index[key];
                    for (const resultIndex in matches) {
                        index++;
                        const match = matches[resultIndex];
                        let className = "";
                        if (index === this.state.selectedIndex) {
                            className = "selected";
                        }
                        entries.push(
                            e(
                                "a",
                                {
                                    className: className,
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
    const searchInput = document.getElementById("search")
    if (searchInput !== null) {
        searchInput.select();
    }
}