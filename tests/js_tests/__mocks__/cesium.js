module.exports = {
    Viewer: jest.fn().mockImplementation(() => ({
      scene: {
        globe: {},
        primitives: { add: jest.fn() },
      },
      camera: {
        setView: jest.fn(),
        flyTo: jest.fn(),
        lookAt: jest.fn(),
        lookAtTransform: jest.fn(),
        viewBoundingSphere: jest.fn(),
      },
      imageryLayers: { addImageryProvider: jest.fn() },
      terrainProvider: jest.fn(),
      entities: { add: jest.fn() },
      clock: {},
      dataSources: { add: jest.fn() },
      trackedEntity: null,
    })),
    Ion: { defaultAccessToken: "mock_token" },
    ClockViewModel: jest.fn(),
    WebMapServiceImageryProvider: jest.fn(),
    JulianDate: {
      fromIso8601: jest.fn(),
      toIso8601: jest.fn(),
    },
    GeoJsonDataSource: {
      load: jest.fn(),
    },
    CzmlDataSource: {
      load: jest.fn(),
    },
    TimeIntervalCollection: {
      fromIso8601DateArray: jest.fn(),
    },
    Cartesian3: jest.fn(),
    Color: jest.fn(),
    HorizontalOrigin: {},
    VerticalOrigin: {},
    PointGraphics: jest.fn(),
    Material: {
      fromType: jest.fn(),
    },
  };
  