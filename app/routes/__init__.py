def register_blueprints(app):
    from .main_routes import bp as main
    from .metrics_routes import bp as metrics
    from .analyze_routes import bp as analyze
    from .predict_routes import bp as predict
    from .history_routes import bp as history
    from .reports_routes import bp as reports
    from .process_routes import bp as processes
    for blueprint in (main, metrics, analyze, predict, history, reports, processes):
        app.register_blueprint(blueprint)
