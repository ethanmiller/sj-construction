var Banner = React.createClass({
	render: function(){
		return (
			<div className='col-md-12'>{this.props.msg}</div>
		);
	}
});

var Filters = React.createClass({
    clickFilter: function(e){
        var filterId = e.target.dataset.id;
		fetch('/subtype_filters/' + filterId + '/')
			.then((response) => {
                return response.json();
            }).then((responseJson) => {
                this.props.setPlaces(responseJson);
			})
    },
	render: function(){
        var filterlist = this.props.filters.map((f) => {
            return <li><a href="#" onClick={this.clickFilter} data-id={f.id}>{f.name}</a></li>
        });
		return (
			<div className='col-md-4'>
                <ul>{filterlist}</ul>
            </div>
		);
	}
});

const mapStyle = {
	width: '800px',
	height: '500px'
};

var Map = React.createClass({
    getInitialState: function (){
        return {
            mapObj: null
        };
    },
	componentDidMount: function(){
        mapboxgl.accessToken = '<api key>';
        var mapx = new mapboxgl.Map({
            container: 'map',
            center: [-121.8761836, 37.3004182],
            zoom: 10,
            style: 'mapbox://styles/mapbox/dark-v9'
        });
        var nav = new mapboxgl.NavigationControl();
        mapx.addControl(nav, 'top-left');
        this.setState({mapObj: mapx});
	},
    componentDidUpdate: function(){
        if(this.props.places.length == 0) return;
        var pointData = [];
        this.props.places.map((f) => {
          pointData.push({
              type: 'Feature',
              geometry: {
                  type: 'Point',
                  coordinates: [parseFloat(f.longitude), parseFloat(f.latitude)]
              },
              properties: {
                  title: f.location,
                  icon: "triangle"
              }
          });
        });
        this.state.mapObj.addLayer({
            id: 'filteredPoints',
            type: 'symbol',
            source: {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: pointData
                }
            },
            layout: {
				"icon-image": "{icon}-11",
				"text-field": "",
				"text-size": 10,
				"text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
				"text-offset": [0, 0.6],
				"text-anchor": "top"
        	}
        });
    },
	render: function(){
            //var marker = new mapboxgl.Marker()
              //.setLngLat([parseFloat(f.longitude), parseFloat(f.latitude)])
              //.addTo(this.state.map);
		return (
			<div className='col-md-8'>
      			<div id='map' style={mapStyle}></div>
			</div>
		);
	}
});

var MapView = React.createClass({
	getInitialState: function() {
		return {
			bannerMsg: "loading ...",
            filtersSubType: [],
            places: []
		};
	},	
	componentDidMount: function(){
		fetch('/init')
			.then((response) => {
                return response.json();
            }).then((responseJson) => {
				this.setState(responseJson);
			})
			.catch((err) => {
				console.log(err);
			});
	},
    setPlaces: function(placesState) {
        this.setState(placesState);
    },
    render: function(){
		return (
			<div className='container'>
				<div className='row'><Banner msg={this.state.bannerMsg} /></div>
				<div className='row'>
                    <Filters filters={this.state.filtersSubType} setPlaces={this.setPlaces} />
                    <Map places={this.state.places} />
                </div>
			</div>
		);
    }
});

ReactDOM.render(<MapView/>, document.body);
