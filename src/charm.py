#!/usr/bin/env python3
# Copyright 2024 Tiexin
# See LICENSE file for licensing details.

"""Charm the application."""

import json
import logging

import ops

logger = logging.getLogger(__name__)


class MyFancyDatabaseCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        self.framework.observe(self.on["httpbin"].pebble_ready, self._on_httpbin_pebble_ready)
        self.framework.observe(
            self.on.database_relation_changed, self._on_database_relation_changed
        )
        self.framework.observe(self.on.database_relation_broken, self._on_database_relation_broken)
        self.framework.observe(self.on.tables_relation_changed, self._on_tables_relation_changed)
        self.framework.observe(self.on.tables_relation_broken, self._on_tables_relation_broken)

    def _on_httpbin_pebble_ready(self, event: ops.PebbleReadyEvent):
        """Handle pebble-ready event."""
        container = event.workload
        container.add_layer("httpbin", self._pebble_layer, combine=True)
        container.replan()
        self.unit.status = ops.ActiveStatus()

    @property
    def _pebble_layer(self) -> ops.pebble.LayerDict:
        """Return a dictionary representing a Pebble layer."""
        return {
            "summary": "httpbin layer",
            "description": "pebble config layer for httpbin",
            "services": {
                "httpbin": {
                    "override": "replace",
                    "summary": "httpbin",
                    "command": "gunicorn -b 0.0.0.0:80 httpbin:app -k gevent",
                    "startup": "enabled",
                    "environment": {
                        "GUNICORN_CMD_ARGS": f"--log-level {self.model.config['log-level']}"
                    },
                }
            },
        }

    def _on_database_relation_changed(self, event: ops.RelationChangedEvent) -> None:
        if self.unit.is_leader():
            event.relation.data[self.app].update({"api_endpoint": "https://example.com/v1/query"})

        event.relation.data[self.unit].update({"secret_id": "secret:123"})

    def _on_database_relation_broken(self, event: ops.RelationBrokenEvent) -> None:
        if self.unit.is_leader():
            event.relation.data[self.app].clear()

        event.relation.data[self.unit].clear()

    def _on_tables_relation_changed(self, event: ops.RelationChangedEvent) -> None:
        if self.unit.is_leader():
            event.relation.data[self.app].update({"tables": json.dumps(["users", "passwords"])})

    def _on_tables_relation_broken(self, event: ops.RelationBrokenEvent) -> None:
        if self.unit.is_leader():
            event.relation.data[self.app].pop("tables")


if __name__ == "__main__":  # pragma: nocover
    ops.main(MyFancyDatabaseCharm)  # type: ignore
