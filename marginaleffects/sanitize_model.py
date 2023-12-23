from .model_abstract import ModelAbstract, ModelStatsmodels


def sanitize_model(model):
    if model is None:
        return model

    if isinstance(model, ModelAbstract):
        return model

    try:
        import statsmodels.base.wrapper as smw

        if isinstance(model, smw.ResultsWrapper):
            return ModelStatsmodels(model)
    except ImportError:
        pass

    raise ValueError(
        "Unknown model type. Try installing the 'statsmodels' package or file an issue at https://github.com/vincentarelbundock/pymarginaleffects."
    )
