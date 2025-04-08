class SEOProtocol:

    def render_title(self, *args, **kwargs) -> str:
        raise NotImplementedError

    def render_description(self, *args, **kwargs) -> str:
        raise NotImplementedError
