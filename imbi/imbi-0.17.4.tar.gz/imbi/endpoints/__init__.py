from tornado import web

from imbi import constants
from . import (activity_feed, authentication_tokens, cookie_cutters, dashboard,
               environments, fact_type_enums, fact_type_ranges, fact_types,
               groups, integrations, metrics, namespaces, openapi, opensearch,
               operations_log, permissions, project_activity_feed,
               project_dependencies, project_fact_history, project_fact_types,
               project_facts, project_link_types, project_links, project_notes,
               project_score_history, project_secrets, project_types,
               project_urls, projects, reports, status, ui)

URLS = [
    web.url(r'^/$', ui.IndexRequestHandler),
    web.url(r'^/activity-feed$', activity_feed.CollectionRequestHandler),
    web.url(r'^/api-docs/$', openapi.RequestHandler),
    web.url(r'^/api-docs/(openapi.yaml)$', openapi.RequestHandler),
    web.url(r'^/authentication-tokens$', authentication_tokens.RequestHandler),
    web.url(
        r'^/authentication-tokens/(?P<token>{})$'.format(
            constants.UUID_PATTERN),
        authentication_tokens.RequestHandler,
    ),
    web.url(r'^/cookie-cutters$', cookie_cutters.CollectionRequestHandler),
    web.url(r'^/cookie-cutters/(?P<name>[\w_\-%\+]+)$',
            cookie_cutters.RecordRequestHandler,
            name='cookie-cutter'),
    web.url(r'^/dashboard$', dashboard.RequestHandler),
    web.url(r'^/environments$', environments.CollectionRequestHandler),
    web.url(r'^/environments/(?P<name>[\w_\-%\+]+)$',
            environments.RecordRequestHandler,
            name='environment'),
    web.url(r'^/groups$', groups.CollectionRequestHandler),
    web.url(r'^/groups/(?P<name>[\w_\-%\+]+)$',
            groups.RecordRequestHandler,
            name='group'),
    web.url(r'^/metrics$', metrics.RequestHandler),
    web.url(r'^/namespaces$', namespaces.CollectionRequestHandler),
    web.url(r'^/namespaces/(?P<id>\d+)$',
            namespaces.RecordRequestHandler,
            name='namespace'),
    web.url(r'^/opensearch/(?P<index>[\w_\-%\+]+)$',
            opensearch.RequestHandler),
    web.url(r'^/operations-log$', operations_log.CollectionRequestHandler),
    web.url(r'^/operations-log/(?P<id>\d+)$',
            operations_log.RecordRequestHandler,
            name='operations-log'),
    web.url(r'^/operations-log/build-search-index',
            operations_log.SearchIndexRequestHandler),
    web.url(r'^/permissions$', permissions.RequestHandler),
    web.url(r'^/project-fact-types$', fact_types.CollectionRequestHandler),
    web.url(r'^/project-fact-types/(?P<id>\d+)$',
            fact_types.RecordRequestHandler,
            name='fact-type'),
    web.url(r'^/project-fact-type-enums$',
            fact_type_enums.CollectionRequestHandler),
    web.url(r'^/project-fact-type-enums/(?P<id>\d+)$',
            fact_type_enums.RecordRequestHandler,
            name='fact-type-enum'),
    web.url(r'^/project-fact-type-ranges$',
            fact_type_ranges.CollectionRequestHandler),
    web.url(r'^/project-fact-type-ranges/(?P<id>\d+)$',
            fact_type_ranges.RecordRequestHandler,
            name='fact-type-range'),
    web.url(r'^/project-link-types$',
            project_link_types.CollectionRequestHandler),
    web.url(r'^/project-link-types/(?P<id>\d+)$',
            project_link_types.RecordRequestHandler,
            name='project-link-type'),
    web.url(r'^/project-types$', project_types.CollectionRequestHandler),
    web.url(r'^/project-types/(?P<id>\d+)$',
            project_types.RecordRequestHandler,
            name='project-type'),
    web.url(r'^/projects/build-search-index',
            projects.SearchIndexRequestHandler),
    web.url(r'^/projects$', projects.CollectionRequestHandler,
            name='projects'),
    web.url(r'^/projects/(?P<id>\d+)$',
            projects.RecordRequestHandler,
            name='project'),
    web.url(r'^/projects/(?P<project_id>\d+)/dependencies$',
            project_dependencies.CollectionRequestHandler,
            name='project-dependencies'),
    web.url(
        r'^/projects/(?P<project_id>\d+)/dependencies/'
        r'(?P<dependency_id>\d+)$',
        project_dependencies.RecordRequestHandler,
        name='project-dependency'),
    web.url(r'^/projects/(?P<project_id>\d+)/facts$',
            project_facts.CollectionRequestHandler,
            name='project-facts'),
    web.url(r'^/projects/(?P<project_id>\d+)/fact-types$',
            project_fact_types.CollectionRequestHandler,
            name='project-fact-types'),
    web.url(r'^/projects/(?P<project_id>\d+)/fact-history$',
            project_fact_history.CollectionRequestHandler,
            name='project-fact-history'),
    web.url(r'^/projects/(?P<project_id>\d+)/feed$',
            project_activity_feed.CollectionRequestHandler,
            name='project-activity-feed'),
    web.url(r'^/projects/(?P<project_id>\d+)/links$',
            project_links.CollectionRequestHandler,
            name='project-links'),
    web.url(r'^/projects/(?P<project_id>\d+)/links/'
            r'(?P<link_type_id>\d+)$',
            project_links.RecordRequestHandler,
            name='project-link'),
    web.url(r'^/projects/(?P<project_id>\d+)/notes$',
            project_notes.CollectionRequestHandler,
            name='project-notes'),
    web.url(r'^/projects/(?P<project_id>\d+)/notes/(?P<id>\d+)$',
            project_notes.RecordHandler,
            name='project-note'),
    web.url(r'^/projects/(?P<project_id>\d+)/score-history$',
            project_score_history.CollectionRequestHandler,
            name='project-score-history'),
    web.url(r'^/projects/(?P<project_id>\d+)/secrets$',
            project_secrets.CollectionRequestHandler,
            name='project-secrets'),
    web.url(r'^/projects/(?P<project_id>\d+)/urls$',
            project_urls.CollectionRequestHandler,
            name='project-urls'),
    web.url(
        r'^/projects/(?P<project_id>\d+)/urls/'
        r'(?P<environment>[\w_\-%\+]+)$',
        project_urls.RecordRequestHandler,
        name='project-url'),
    web.url(r'^/status$', status.RequestHandler),
] + integrations.URLS + ui.URLS + reports.URLS
