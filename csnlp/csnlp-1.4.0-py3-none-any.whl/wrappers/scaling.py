from typing import Dict, Iterable, List, Literal, Optional, Tuple, TypeVar, Union
from warnings import warn

import casadi as cs
import numpy as np
import numpy.typing as npt

from csnlp.core.scaling import Scaler
from csnlp.core.solutions import Solution, subsevalf
from csnlp.wrappers.wrapper import Nlp, NonRetroactiveWrapper

T = TypeVar("T", cs.SX, cs.MX)


class NlpScaling(NonRetroactiveWrapper[T]):
    def __init__(self, nlp: Nlp[T], scaler: Scaler, warns: bool = True) -> None:
        super().__init__(nlp)
        self.scaler = scaler
        self.warns = warns
        self._svars: Dict[str, T] = {}
        self._spars: Dict[str, T] = {}
        self._uvars: Dict[str, T] = {}
        self._upars: Dict[str, T] = {}

    @property
    def scaled_variables(self) -> Dict[str, T]:
        """Gets the scaled variables of the NLP scheme."""
        return self._svars

    @property
    def scaled_parameters(self) -> Dict[str, T]:
        """Gets the scaled parameters of the NLP scheme."""
        return self._spars

    @property
    def unscaled_variables(self) -> Dict[str, T]:
        """Gets the unscaled variables of the NLP scheme."""
        return self._uvars

    @property
    def unscaled_parameters(self) -> Dict[str, T]:
        """Gets the unscaled parameters of the NLP scheme."""
        return self._upars

    def scale(self, expr: T) -> T:
        """Scales an expression with the MPC's scaled variables and parameters.

        Parameters
        ----------
        expr : casadi.SX or MX
            The expression to be scaled.

        Returns
        -------
        casadi.SX or MX
            The scaled expression.
        """
        expr = subsevalf(expr, self.nlp.variables, self._svars, eval=False)
        expr = subsevalf(expr, self.nlp.parameters, self._spars, eval=False)
        return expr

    def unscale(self, expr: T) -> T:
        """Unscales an expression with the MPC's unscaled variables and parameters.

        Parameters
        ----------
        expr : casadi.SX or MX
            The expression to be unscaled.

        Returns
        -------
        casadi.SX or MX
            The unscaled expression.
        """
        expr = subsevalf(expr, self.nlp.variables, self._uvars, eval=False)
        expr = subsevalf(expr, self.nlp.parameters, self._upars, eval=False)
        return expr

    def variable(
        self,
        name: str,
        shape: Tuple[int, int] = (1, 1),
        lb: Union[npt.ArrayLike, cs.DM] = -np.inf,
        ub: Union[npt.ArrayLike, cs.DM] = +np.inf,
    ) -> Tuple[T, T, T]:
        """See `Nlp.variable` method."""
        can_scale = name in self.scaler
        if can_scale:
            lb, ub = np.broadcast_to(lb, shape), np.broadcast_to(ub, shape)
            lb = self.scaler.scale(name, lb)
            ub = self.scaler.scale(name, ub)
        var, lam_lb, lam_ub = self.nlp.variable(name, shape, lb, ub)
        if can_scale:
            svar = self.scaler.scale(name, var)
            uvar = self.scaler.unscale(name, var)
        else:
            if self.warns:
                warn(f"Scaling for variable {name} not found.", RuntimeWarning)
            svar = uvar = var
        self._svars[name] = svar
        self._uvars[name] = uvar
        return var, lam_lb, lam_ub

    def parameter(self, name: str, shape: Tuple[int, int] = (1, 1)) -> T:
        """See `Nlp.parameter` method."""
        par = self.nlp.parameter(name, shape)
        if name in self.scaler:
            spar = self.scaler.scale(name, par)
            upar = self.scaler.unscale(name, par)
        else:
            if self.warns:
                warn(f"Scaling for parameter {name} not found.", RuntimeWarning)
            spar = upar = par
        self._spars[name] = spar
        self._upars[name] = upar
        return par

    def constraint(
        self,
        name: str,
        lhs: Union[T, np.ndarray, cs.DM],
        op: Literal["==", ">=", "<="],
        rhs: Union[T, np.ndarray, cs.DM],
        soft: bool = False,
        simplify: bool = True,
    ) -> Tuple[T, ...]:
        """See `Nlp.constraint` method."""
        return self.nlp.constraint(
            name, self.unscale(lhs - rhs), op, 0, soft=soft, simplify=simplify
        )

    def minimize(self, objective: T) -> None:
        """See `Nlp.minimize` method."""
        return self.nlp.minimize(self.unscale(objective))

    def solve(
        self,
        pars: Optional[Dict[str, npt.ArrayLike]] = None,
        vals0: Optional[Dict[str, npt.ArrayLike]] = None,
    ) -> Solution[T]:
        """See `Nlp.solve` method."""
        if pars is not None:
            pars = self._scale_dict(pars)
        if vals0 is not None:
            vals0 = self._scale_dict(vals0)
        return self.nlp.solve(pars, vals0)

    def solve_multi(
        self,
        pars: Union[
            None, Dict[str, npt.ArrayLike], Iterable[Dict[str, npt.ArrayLike]]
        ] = None,
        vals0: Union[
            None, Dict[str, npt.ArrayLike], Iterable[Dict[str, npt.ArrayLike]]
        ] = None,
        return_all_sols: bool = False,
        return_multi_sol: bool = False,
    ) -> Union[Solution[T], List[Solution[T]]]:
        """See `MultistartNlp.solve` method."""
        assert (
            self.nlp.is_multi
        ), "`solve_multi` called on an nlp instance that is not `MultistartNlp`."
        if pars is not None:
            pars = (
                self._scale_dict(pars)
                if isinstance(pars, dict)
                else (self._scale_dict(pars_i) for pars_i in pars)
            )
        if vals0 is not None:
            vals0 = (
                self._scale_dict(vals0)
                if isinstance(vals0, dict)
                else (self._scale_dict(vals0_i) for vals0_i in vals0)
            )
        return self.nlp.solve_multi(  # type: ignore
            pars,
            vals0,
            return_all_sols=return_all_sols,
            return_multi_sol=return_multi_sol,
        )

    def _scale_dict(self, d: Dict[str, npt.ArrayLike]) -> Dict[str, npt.ArrayLike]:
        # sourcery skip: remove-dict-keys
        """Internal utility for scaling structures/dicts."""
        scaler = self.scaler
        return {
            name: scaler.scale(name, d[name]) if scaler.can_scale(name) else d[name]
            for name in d.keys()
        }
